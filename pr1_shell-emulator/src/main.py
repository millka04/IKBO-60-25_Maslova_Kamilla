"""Точка входа: читает параметры и открывает окно эмулятора."""

from st_args import parse_args, show_params
from gui import App
from script import run_script
from shell import Shell
from vfs import Vfs, VfsError

SCRIPT_DELAY_MS = 100

def load_vfs(path):
    """Загружает VFS из архива. Возвращает (vfs, текст ошибки)."""
    if not path:
        return Vfs(), ""
    try:
        return Vfs.from_zip(path), ""
    except VfsError as error:
        return Vfs(), f"Ошибка загрузки VFS: {error}. Используется пустая VFS."

def main():
    """Запускает эмулятор с параметрами из командной строки."""
    args = parse_args()
    vfs, error = load_vfs(args.vfs)
    shell = Shell(vfs)
    app = App(shell)
    show_params(app, args)
    app.write(error)
    if args.script:
        app.root.after(SCRIPT_DELAY_MS, run_script, app, args.script)
    app.start()


if __name__ == "__main__":
    main()