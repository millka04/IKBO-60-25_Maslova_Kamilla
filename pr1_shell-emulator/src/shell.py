"""Ядро эмулятора: хранит состояние и выполняет команды."""

import getpass
import socket

from cmdparse import parse_line
from commands import COMMANDS
from errors import ShellError
from vfs import Vfs, VfsError


class Shell:
    """Состояние эмулятора и выполнение введённых строк."""

    def __init__(self, vfs=None):
        """Запоминает имя пользователя и компьютера из реальной ОС."""
        self.user = getpass.getuser()
        self.host = socket.gethostname()
        self.running = True
        self.vfs = vfs or Vfs()
        self.cwd = self.vfs.root

    def title(self):
        """Возвращает заголовок окна вида Эмулятор - [user@host]."""
        return f"Эмулятор - [{self.user}@{self.host}]"

    def prompt(self):
        """Возвращает приглашение командной строки."""
        return f"{self.user}@{self.host}:{self.cwd.path()}$ "

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
        try:
            return handler(self, args)
        except VfsError as error:
            raise ShellError(f"{name}: {error}") from error