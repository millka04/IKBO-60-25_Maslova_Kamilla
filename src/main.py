"""Точка входа: создаёт эмулятор и открывает его окно."""

from gui import App
from shell import Shell


def main():
    """Запускает эмулятор в графическом окне."""
    shell = Shell()
    app = App(shell)
    app.write("Эмулятор запущен. Команды: ls, cd, exit.")
    app.start()


if __name__ == "__main__":
    main()