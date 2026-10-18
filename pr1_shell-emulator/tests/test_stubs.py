"""Тесты команд-заглушек ls и cd (этап 1)."""

import unittest

from shell import Shell


class StubTest(unittest.TestCase):
    """Заглушки выводят своё имя и аргументы."""

    def test_ls_stub(self):
        """ls выводит имя и аргументы."""
        result = Shell().execute("ls -l /home")
        self.assertEqual(result, "Команда: ls, аргументы: ['-l', '/home']")

    def test_cd_stub(self):
        """cd без аргументов выводит пустой список."""
        self.assertEqual(Shell().execute("cd"), "Команда: cd, аргументы: []")