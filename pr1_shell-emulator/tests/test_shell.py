"""Тесты ядра эмулятора: разбор строки, exit, ошибки."""

import getpass
import unittest

from cmdparse import parse_line
from errors import ShellError
from shell import Shell


class ParseTest(unittest.TestCase):
    """Проверки простого парсера."""

    def test_split_by_spaces(self):
        """Строка делится на слова по пробелам."""
        self.assertEqual(parse_line("ls  -l  /home"), ["ls", "-l", "/home"])

    def test_empty_line(self):
        """Пустая строка даёт пустой список."""
        self.assertEqual(parse_line("   "), [])


class ShellTest(unittest.TestCase):
    """Проверки выполнения команд."""

    def setUp(self):
        """Создаёт новый эмулятор перед каждым тестом."""
        self.shell = Shell()

    def test_title_has_user(self):
        """Заголовок окна содержит имя пользователя ОС."""
        self.assertIn(getpass.getuser(), self.shell.title())

    def test_empty_line(self):
        """Пустая строка ничего не выводит."""
        self.assertEqual(self.shell.execute(""), "")

    def test_unknown_command(self):
        """Неизвестная команда вызывает ошибку."""
        with self.assertRaises(ShellError):
            self.shell.execute("hello world")

    def test_exit(self):
        """Команда exit останавливает эмулятор."""
        self.shell.execute("exit")
        self.assertFalse(self.shell.running)

    def test_exit_with_args(self):
        """exit с аргументами - ошибка, эмулятор продолжает работу."""
        with self.assertRaises(ShellError):
            self.shell.execute("exit 5")
        self.assertTrue(self.shell.running)
