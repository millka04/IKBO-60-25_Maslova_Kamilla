"""Инструмент визуализации графа зависимостей пакетов Cargo."""

import argparse
import sys
from typing import Any


from config import load_config
from errors import ToolError
from graph import GraphBuilder
from sources import (
    CargoSource,
    DependencySource,
    DictSource,
    load_repository_file,
)

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


def create_source(config: dict[str, Any]) -> DependencySource:
    """Выбирает источник данных: интернет или тестовый файл."""
    if config["test_mode"]:
        return DictSource(load_repository_file(config["repository"]))
    return CargoSource(config["repository"])


def print_graph(graph: dict[str, list[str]]) -> None:
    """Печатает граф: пакет -> его зависимости."""
    for name, dependencies in graph.items():
        text: str = " ".join(dependencies)
        print(f"{name} -> {text}")


def run(config_path: str) -> None:
    """Строит граф зависимостей и выводит его."""
    config: dict[str, Any] = load_config(config_path)
    source: DependencySource = create_source(config)
    builder = GraphBuilder(source, config["max_depth"], config["filter"])
    graph: dict[str, list[str]] = builder.build(config["package"])
    print_graph(graph)


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
