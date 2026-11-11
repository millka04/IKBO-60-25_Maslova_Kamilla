"""Получение зависимостей пакетов Cargo из индекса crates.io."""

import json
import urllib.error
import urllib.request
from typing import Any

from errors import ToolError

USER_AGENT: str = "student-dependency-graph"
TIMEOUT: int = 20
HTTP_NOT_FOUND: int = 404
LENGTH_ONE: int = 1
LENGTH_TWO: int = 2
LENGTH_THREE: int = 3
PREFIX_SIZE: int = 2
NORMAL_KIND: str = "normal"


def make_index_path(name: str) -> str:
    """Строит путь к файлу пакета в индексе crates.io."""
    name = name.lower()
    if len(name) == LENGTH_ONE:
        return "1/" + name
    if len(name) == LENGTH_TWO:
        return "2/" + name
    if len(name) == LENGTH_THREE:
        return "3/" + name[0] + "/" + name
    first: str = name[:PREFIX_SIZE]
    second: str = name[PREFIX_SIZE:PREFIX_SIZE * 2]
    return first + "/" + second + "/" + name


def download_text(url: str) -> str:
    """Скачивает текст по адресу url."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        if error.code == HTTP_NOT_FOUND:
            raise ToolError(f"Пакет не найден: {url}") from error
        raise ToolError(f"Ошибка сервера {error.code}: {url}") from error
    except urllib.error.URLError as error:
        raise ToolError(f"Нет доступа к {url}: {error.reason}") from error
    except ValueError as error:
        raise ToolError(f"Неверный адрес: {url}") from error


def parse_line(line: str) -> dict[str, Any]:
    """Разбирает одну строку индекса (одну версию пакета)."""
    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        raise ToolError("Индекс содержит неверные данные") from error


def find_latest_version(text: str) -> dict[str, Any]:
    """Находит последнюю версию без отзыва и без пометки пре-релиза."""
    latest: dict[str, Any] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        info: dict[str, Any] = parse_line(line)
        if info.get("yanked") or "-" in info["vers"]:
            continue
        latest = info
    if not latest:
        raise ToolError("Не найдена подходящая версия пакета")
    return latest


def get_normal_dependencies(info: dict[str, Any]) -> list[str]:
    """Возвращает имена обычных обязательных зависимостей версии."""
    names: list[str] = []
    for dep in info["deps"]:
        kind: str = dep.get("kind") or NORMAL_KIND
        if kind != NORMAL_KIND or dep.get("optional"):
            continue
        real_name: str = dep.get("package") or dep["name"]
        if real_name not in names:
            names.append(real_name)
    return names


def get_direct_dependencies(base_url: str, package: str) -> list[str]:
    """Возвращает прямые зависимости последней версии пакета."""
    url: str = base_url.rstrip("/") + "/" + make_index_path(package)
    text: str = download_text(url)
    info: dict[str, Any] = find_latest_version(text)
    return get_normal_dependencies(info)
