"""Источники данных о зависимостях: интернет и тестовый файл."""

import re

from cargo_source import get_direct_dependencies
from errors import ToolError

NAME_PATTERN: str = r"^[A-Z]+$"
SEPARATOR: str = ":"


class DependencySource:
    """Базовый класс: умеет возвращать прямые зависимости пакета."""

    def get_dependencies(self, name: str) -> list[str]:
        """Возвращает прямые зависимости пакета."""
        raise NotImplementedError


class CargoSource(DependencySource):
    """Источник: индекс crates.io в интернете."""

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url

    def get_dependencies(self, name: str) -> list[str]:
        return get_direct_dependencies(self.base_url, name)


class DictSource(DependencySource):
    """Источник: словарь 'пакет -> список зависимостей'."""

    def __init__(self, repository: dict[str, list[str]]) -> None:
        self.repository: dict[str, list[str]] = repository

    def get_dependencies(self, name: str) -> list[str]:
        if name not in self.repository:
            raise ToolError(f"Пакет {name} не найден в репозитории")
        return self.repository[name]


def check_name(name: str) -> None:
    """Проверяет, что имя состоит из больших латинских букв."""
    if re.match(NAME_PATTERN, name) is None:
        raise ToolError(f"Неверное имя пакета в тестовом файле: '{name}'")


def parse_repository_text(text: str) -> dict[str, list[str]]:
    """Превращает текст тестового файла в словарь."""
    repository: dict[str, list[str]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        name, separator, rest = line.partition(SEPARATOR)
        if not separator:
            raise ToolError(f"В строке нет двоеточия: '{line}'")
        name = name.strip()
        dependencies: list[str] = rest.split()
        check_name(name)
        for dependency in dependencies:
            check_name(dependency)
        repository[name] = dependencies
    return repository


def load_repository_file(path: str) -> dict[str, list[str]]:
    """Читает тестовый файл и возвращает словарь."""
    try:
        with open(path, encoding="utf-8") as file:
            text: str = file.read()
    except OSError as error:
        raise ToolError(f"Не удалось прочитать файл {path}") from error
    return parse_repository_text(text)
