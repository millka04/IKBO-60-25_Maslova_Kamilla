"""Выполнение стартового скрипта эмулятора."""


def read_script(path):
    """Читает файл скрипта и возвращает список его строк."""
    with open(path, encoding="utf-8") as file:
        return file.read().splitlines()


def is_command(line):
    """Проверяет, что строка не пустая и не комментарий (#)."""
    text = line.strip()
    return bool(text) and not text.startswith("#")


def run_script(app, path):
    """Выполняет команды скрипта по очереди, как будто их вводит человек.

    Строки с ошибками пропускаются: выводится сообщение об ошибке,
    и выполнение продолжается со следующей строки.
    """
    try:
        lines = read_script(path)
    except OSError as error:
        app.write(f"Ошибка: не удалось открыть скрипт {path}: "
                  f"{error.strerror}")
        return
    for line in lines:
        if not is_command(line):
            continue
        app.run_line(line)
        if not app.shell.running:
            return