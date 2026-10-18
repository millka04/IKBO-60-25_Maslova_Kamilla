"""Ядро эмулятора: хранит состояние и выполняет команды."""

import getpass
import socket

from cmdparse import parse_line
from commands import COMMANDS
from errors import ShellError


class Shell:
    """Состояние эмулятора и выполнение введённых строк."""

    def __init__(self):
        """Запоминает имя пользователя и компьютера из реальной ОС."""
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.running = True

    def title(self):
        """Возвращает заголовок окна вида Эмулятор - [user@host]."""
        return f"Эмулятор - [{self.user}@{self.host}]"

    def prompt(self):
        """Возвращает приглашение командной строки."""
        return f"{self.user}@{self.host}:~$ "

    def execute(self, line):
        """Выполняет одну строку и возвращает текст результата.

        При ошибке выбрасывает ShellError с понятным сообщением.
        """
        words = parse_line(line)
        if not words:
            return ""
        name, args = words[0], words[1:]
        handler = COMMANDS.get(name)
        if handler is None:
            raise ShellError(f"{name}: команда не найдена")
        return handler(self, args)