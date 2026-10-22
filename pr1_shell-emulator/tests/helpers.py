"""Общие функции для тестов."""

import os
import tempfile
import zipfile

from shell import Shell
from vfs import Vfs

SAMPLE = {
    "readme.txt": b"hello\n",
    "home/user/notes.txt": "".join(
        f"line {number}\n" for number in range(1, 16)).encode(),
    "home/user/docs/report.txt": b"Report\n",
    "bin/tool.bin": bytes(range(256)),
}


def make_zip(files):
    """Создаёт временный ZIP-архив и возвращает путь к нему."""
    handle, path = tempfile.mkstemp(suffix=".zip")
    os.close(handle)
    with zipfile.ZipFile(path, "w") as archive:
        for inner_path, data in files.items():
            archive.writestr(inner_path, data)
    return path


def make_shell(files=None):
    """Создаёт эмулятор с VFS из словаря файлов (по умолчанию SAMPLE)."""
    path = make_zip(SAMPLE if files is None else files)
    vfs = Vfs.from_zip(path)
    os.remove(path)
    return Shell(vfs)