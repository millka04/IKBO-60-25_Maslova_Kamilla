"""Команды эмулятора и таблица соответствия имён и функций."""

from errors import ShellError


def stub(name, args):
    """Заглушка: возвращает имя команды и её аргументы."""
    return f"Команда: {name}, аргументы: {args}"


def cmd_ls(shell, args):
    """Заглушка команды ls."""
    return stub("ls", args)


def cmd_cd(shell, args):
    """Заглушка команды cd."""
    return stub("cd", args)


def cmd_exit(shell, args):
    """Завершает работу эмулятора. Аргументы не принимает."""
    if args:
        raise ShellError("exit: команда не принимает аргументы")
    shell.running = False
    return ""


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}