"""Тесты стартового скрипта и параметров командной строки."""

import os
import tempfile
import unittest

from st_args import parse_args
from errors import ShellError
from script import run_script
from shell import Shell


class FakeApp:
    """Замена окна: запоминает вывод вместо показа на экране."""

    def __init__(self):
        """Создаёт эмулятор и пустой список вывода."""
        self.shell = Shell()
        self.lines = []

    def write(self, text):
        """Запоминает выведенный текст."""
        self.lines.append(text)

    def run_line(self, line):
        """Выполняет строку так же, как настоящее окно."""
        self.write("$ " + line)
        try:
            self.write(self.shell.execute(line))
        except ShellError as error:
            self.write(f"Ошибка: {error}")


def write_temp(text):
    """Создаёт временный файл с текстом и возвращает путь к нему."""
    handle, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(handle, "w", encoding="utf-8") as file:
        file.write(text)
    return path


class ScriptTest(unittest.TestCase):
    """Проверки выполнения стартового скрипта."""

    def test_errors_are_skipped(self):
        """Ошибочная строка не останавливает скрипт."""
        path = write_temp("# комментарий\nwrong\n\nls a\n")
        app = FakeApp()
        run_script(app, path)
        os.remove(path)
        self.assertIn("Ошибка: wrong: команда не найдена", app.lines)
        self.assertIn("$ ls a", app.lines)
        self.assertNotIn("$ # комментарий", app.lines)

    def test_exit_stops_script(self):
        """После exit следующие строки не выполняются."""
        path = write_temp("exit\nls\n")
        app = FakeApp()
        run_script(app, path)
        os.remove(path)
        self.assertNotIn("$ ls", app.lines)

    def test_missing_script(self):
        """Несуществующий скрипт даёт сообщение об ошибке."""
        app = FakeApp()
        run_script(app, "no_such_file.txt")
        self.assertTrue(app.lines[0].startswith("Ошибка"))


class ArgsTest(unittest.TestCase):
    """Проверки разбора параметров командной строки."""

    def test_both_params(self):
        """Оба параметра читаются."""
        args = parse_args(["--vfs", "a.zip", "--script", "s.txt"])
        self.assertEqual((args.vfs, args.script), ("a.zip", "s.txt"))

    def test_no_params(self):
        """Без параметров значения равны None."""
        args = parse_args([])
        self.assertIsNone(args.vfs)
        self.assertIsNone(args.script)