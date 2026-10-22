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

def cmd_vfs_info(shell, args):
    """Выводит имя загруженной VFS и SHA-256 хеш её данных."""
    if args:
        raise ShellError("vfs-info: команда не принимает аргументы")
    return f"Имя VFS: {shell.vfs.name}\nSHA-256: {shell.vfs.sha256}"


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
    "vfs-info": cmd_vfs_info,
}