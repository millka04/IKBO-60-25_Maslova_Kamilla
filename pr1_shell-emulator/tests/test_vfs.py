"""Тесты загрузки VFS и команды vfs-info."""

import hashlib
import os
import unittest

from errors import ShellError
from helpers import SAMPLE, make_shell, make_zip
from vfs import Vfs, VfsError


class VfsLoadTest(unittest.TestCase):
    """Проверки загрузки VFS из ZIP-архива."""

    def test_tree_is_built(self):
        """Вложенные папки и файлы появляются в дереве."""
        shell = make_shell()
        node = shell.vfs.resolve(shell.cwd, "/home/user/docs/report.txt")
        self.assertEqual(node.data, b"Report\n")
        self.assertTrue(node.parent.is_dir)

    def test_sha256(self):
        """Хеш совпадает с SHA-256 байтов архива."""
        path = make_zip(SAMPLE)
        with open(path, "rb") as file:
            expected = hashlib.sha256(file.read()).hexdigest()
        vfs = Vfs.from_zip(path)
        os.remove(path)
        self.assertEqual(vfs.sha256, expected)

    def test_missing_file(self):
        """Несуществующий архив вызывает VfsError."""
        with self.assertRaises(VfsError):
            Vfs.from_zip("no_such.zip")

    def test_not_zip(self):
        """Файл, который не является архивом, вызывает VfsError."""
        path = make_zip(SAMPLE)
        with open(path, "w", encoding="utf-8") as file:
            file.write("not a zip")
        with self.assertRaises(VfsError):
            Vfs.from_zip(path)
        os.remove(path)


class VfsInfoTest(unittest.TestCase):
    """Проверки служебной команды vfs-info."""

    def test_info(self):
        """vfs-info выводит имя и хеш."""
        shell = make_shell()
        result = shell.execute("vfs-info")
        self.assertIn(shell.vfs.name, result)
        self.assertIn(shell.vfs.sha256, result)

    def test_info_with_args(self):
        """vfs-info с аргументами - ошибка."""
        with self.assertRaises(ShellError):
            make_shell().execute("vfs-info x")