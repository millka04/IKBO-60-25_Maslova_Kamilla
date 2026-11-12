"""Инструмент визуализации графа зависимостей пакетов Cargo."""

import argparse
import sys
from typing import Any


from config import load_config
from errors import ToolError
from graph import GraphBuilder
from reverse import find_reverse_dependencies
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
    parser.add_argument(
        "--reverse",
        default="",
        help="показать пакеты, которые зависят от этого пакета",
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


def print_reverse(graph: dict[str, list[str]], target: str) -> None:
    """Печатает пакеты, которые зависят от target."""
    names: list[str] = find_reverse_dependencies(graph, target)
    if not names:
        print(f"От пакета {target} никто не зависит")
        return
    print(f"От пакета {target} зависят:")
    for name in names:
        print(name)


def run(config_path: str, reverse_target: str) -> None:
    """Строит граф и выводит его или обратные зависимости."""
    config: dict[str, Any] = load_config(config_path)
    source: DependencySource = create_source(config)
    builder = GraphBuilder(source, config["max_depth"], config["filter"])
    graph: dict[str, list[str]] = builder.build(config["package"])
    if reverse_target:
        print_reverse(graph, reverse_target)
    else:
        print_graph(graph)


def main() -> int:
    """Запускает программу и возвращает код завершения."""
    arguments: argparse.Namespace = parse_arguments()
    try:
        run(arguments.config, arguments.reverse)
    except ToolError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
