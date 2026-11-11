"""Инструмент визуализации графа зависимостей пакетов Cargo."""

import argparse
import sys
from typing import Any

from config import load_config
from errors import ToolError

EXIT_OK: int = 0
EXIT_ERROR: int = 1


def parse_arguments() -> argparse.Namespace:
    """Читает аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Граф зависимостей Cargo")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="путь к файлу конфигурации YAML",
    )
    return parser.parse_args()


def run(config_path: str) -> None:
    """Выводит все параметры конфигурации."""
    config: dict[str, Any] = load_config(config_path)
    for key, value in config.items():
        print(f"{key}: {value}")


def main() -> int:
    """Запускает программу и возвращает код завершения."""
    arguments: argparse.Namespace = parse_arguments()
    try:
        run(arguments.config)
    except ToolError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
