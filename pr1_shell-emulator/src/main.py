"""Точка входа: читает параметры и открывает окно эмулятора."""

from st_args import parse_args, show_params
from gui import App
from script import run_script
from shell import Shell

SCRIPT_DELAY_MS = 100

def main():
    """Запускает эмулятор с параметрами из командной строки."""
    args = parse_args()
    shell = Shell()
    app = App(shell)
    show_params(app, args)
    if args.script:
        app.root.after(SCRIPT_DELAY_MS, run_script, app, args.script)
    app.start()


if __name__ == "__main__":
    main()