"""Параметры командной строки эмулятора и их отладочный вывод."""

import argparse


def parse_args(argv=None):
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор командной строки UNIX (вариант 19)")
    parser.add_argument("--vfs", help="путь к ZIP-архиву с VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args(argv)


def show_params(app, args):
    """Отладочный вывод всех параметров в окно и в терминал."""
    app.write("Параметры запуска:")
    for key, value in vars(args).items():
        line = f"  {key} = {value}"
        print(line)
        app.write(line)