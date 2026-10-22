"""Виртуальная файловая система (VFS), которая целиком живёт в памяти.

Источник VFS - ZIP-архив. Архив читается в память и никогда
не распаковывается на диск и не изменяется.
"""

import hashlib
import io
import os
import zipfile

DIR_MODE = 0o755
FILE_MODE = 0o644
MODE_LETTERS = "rwxrwxrwx"
OWNER_READ = 0o400


class VfsError(Exception):
    """Ошибка работы с VFS."""


class Node:
    """Файл или папка внутри VFS."""

    def __init__(self, name, is_dir, parent=None, data=b""):
        """Создаёт узел. Для папок data не используется."""
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.data = data
        self.children = {}
        self.mode = DIR_MODE if is_dir else FILE_MODE

    def path(self):
        """Возвращает полный путь узла."""
        parts = []
        node = self
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))

    def mode_string(self):
        """Возвращает права в виде строки, например drwxr-xr-x."""
        kind = "d" if self.is_dir else "-"
        letters = [
            letter if self.mode & (OWNER_READ >> index) else "-"
            for index, letter in enumerate(MODE_LETTERS)
        ]
        return kind + "".join(letters)


class Vfs:
    """Дерево файлов и папок, загруженное в память."""

    def __init__(self, name="пустая VFS", raw=b""):
        """Создаёт пустую VFS с именем и хешем исходных данных."""
        self.name = name
        self.sha256 = hashlib.sha256(raw).hexdigest()
        self.root = Node("", True)

    @classmethod
    def from_zip(cls, path):
        """Читает ZIP-архив в память и строит по нему дерево VFS."""
        try:
            with open(path, "rb") as file:
                raw = file.read()
            archive = zipfile.ZipFile(io.BytesIO(raw))
        except OSError as error:
            raise VfsError(f"не удалось открыть {path}: "
                           f"{error.strerror}") from error
        except zipfile.BadZipFile as error:
            raise VfsError(f"{path} не является ZIP-архивом") from error
        vfs = cls(os.path.basename(path), raw)
        for info in archive.infolist():
            vfs.add_entry(info, archive)
        return vfs

    def add_entry(self, info, archive):
        """Добавляет в дерево один элемент архива."""
        parts = [part for part in info.filename.split("/") if part]
        if not parts:
            return
        folder = self.make_dirs(parts[:-1])
        if info.is_dir():
            self.make_dirs(parts)
            return
        data = archive.read(info)
        folder.children[parts[-1]] = Node(parts[-1], False, folder, data)

    def make_dirs(self, parts):
        """Создаёт цепочку папок (если их нет) и возвращает последнюю."""
        node = self.root
        for part in parts:
            if part not in node.children:
                node.children[part] = Node(part, True, node)
            node = node.children[part]
        return node

    def resolve(self, cwd, path):
        """Находит узел по абсолютному или относительному пути."""
        node = self.root if path.startswith("/") else cwd
        for part in path.split("/"):
            node = self.step(node, part, path)
        return node

    def step(self, node, part, path):
        """Делает один шаг по пути: ., .. или имя вложенного элемента."""
        if part in ("", "."):
            return node
        if part == "..":
            return node.parent or node
        if not node.is_dir:
            raise VfsError(f"{path}: не является папкой")
        child = node.children.get(part)
        if child is None:
            raise VfsError(f"{path}: нет такого файла или папки")
        return child