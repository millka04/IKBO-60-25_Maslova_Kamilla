"""Чтение и проверка конфигурационного файла YAML."""

import os
import re
from typing import Any

import yaml

from errors import ToolError

REQUIRED_KEYS: list[str] = [
    "package",
    "repository",
    "test_mode",
    "output_file",
    "max_depth",
    "filter",
]
MIN_DEPTH: int = 0
PNG_EXTENSION: str = ".png"
URL_PREFIXES: tuple[str, str] = ("http://", "https://")
PACKAGE_PATTERN: str = r"^[A-Za-z0-9_-]+$"
TEST_PACKAGE_PATTERN: str = r"^[A-Z]+$"


def read_yaml(path: str) -> Any:
    """Читает YAML-файл и возвращает его содержимое."""
    if not os.path.isfile(path):
        raise ToolError(f"Файл конфигурации не найден: {path}")
    try:
        with open(path, encoding="utf-8") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ToolError(f"Ошибка синтаксиса YAML: {error}") from error
    except OSError as error:
        raise ToolError(f"Не удалось прочитать файл: {error}") from error


def check_keys(data: dict[str, Any]) -> None:
    """Проверяет, что все нужные параметры есть в файле."""
    for key in REQUIRED_KEYS:
        if key not in data:
            raise ToolError(f"Не задан параметр: {key}")


def check_text(data: dict[str, Any], key: str) -> str:
    """Проверяет, что параметр является непустой строкой."""
    value: Any = data[key]
    if not isinstance(value, str) or not value:
        raise ToolError(f"{key}: нужна непустая строка")
    return value


def check_mode(data: dict[str, Any]) -> None:
    """Проверяет параметр test_mode."""
    if not isinstance(data["test_mode"], bool):
        raise ToolError("test_mode: нужно значение true или false")


def check_package(data: dict[str, Any]) -> None:
    """Проверяет имя пакета."""
    package: str = check_text(data, "package")
    pattern: str = PACKAGE_PATTERN
    if data["test_mode"]:
        pattern = TEST_PACKAGE_PATTERN
    if re.match(pattern, package) is None:
        raise ToolError(f"package: недопустимое имя '{package}'")


def check_repository(data: dict[str, Any]) -> None:
    """Проверяет адрес репозитория или путь к тестовому файлу."""
    repository: str = check_text(data, "repository")
    if data["test_mode"]:
        if not os.path.isfile(repository):
            raise ToolError(f"repository: файл не найден: {repository}")
    elif not repository.startswith(URL_PREFIXES):
        raise ToolError("repository: адрес должен начинаться с http(s)://")


def check_output_file(data: dict[str, Any]) -> None:
    """Проверяет имя файла с картинкой."""
    output_file: str = check_text(data, "output_file")
    if not output_file.endswith(PNG_EXTENSION):
        raise ToolError("output_file: имя должно заканчиваться на .png")


def check_depth(data: dict[str, Any]) -> None:
    """Проверяет максимальную глубину."""
    depth: Any = data["max_depth"]
    if isinstance(depth, bool) or not isinstance(depth, int):
        raise ToolError("max_depth: нужно целое число")
    if depth < MIN_DEPTH:
        raise ToolError(f"max_depth: число не меньше {MIN_DEPTH}")


def check_filter(data: dict[str, Any]) -> None:
    """Проверяет подстроку для фильтрации."""
    if not isinstance(data["filter"], str):
        raise ToolError("filter: нужна строка (может быть пустой)")


def load_config(path: str) -> dict[str, Any]:
    """Читает конфигурацию и проверяет все параметры."""
    data: Any = read_yaml(path)
    if not isinstance(data, dict):
        raise ToolError("Файл должен содержать пары 'параметр: значение'")
    check_keys(data)
    check_mode(data)
    check_package(data)
    check_repository(data)
    check_output_file(data)
    check_depth(data)
    check_filter(data)
    return data
