"""Тесты построения графа зависимостей."""

import pytest

from errors import ToolError
from graph import GraphBuilder
from sources import DictSource, parse_repository_text

BIG_DEPTH: int = 10
NO_FILTER: str = ""


def build(
    repository: dict[str, list[str]],
    root: str,
    max_depth: int,
    substring: str,
) -> dict[str, list[str]]:
    """Строит граф для тестового репозитория."""
    builder = GraphBuilder(DictSource(repository), max_depth, substring)
    return builder.build(root)


def test_chain() -> None:
    """Цепочка без циклов."""
    repository = {"A": ["B"], "B": ["C"], "C": []}
    assert build(repository, "A", BIG_DEPTH, NO_FILTER) == repository


def test_diamond() -> None:
    """Общая зависимость попадает в граф один раз."""
    repository = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    assert build(repository, "A", BIG_DEPTH, NO_FILTER) == repository


def test_cycle() -> None:
    """Цикл не приводит к бесконечной рекурсии."""
    repository = {"A": ["B"], "B": ["C"], "C": ["A"]}
    assert build(repository, "A", BIG_DEPTH, NO_FILTER) == repository


def test_self_loop() -> None:
    """Пакет, зависящий от самого себя."""
    repository = {"A": ["A"]}
    assert build(repository, "A", BIG_DEPTH, NO_FILTER) == repository


def test_depth_zero() -> None:
    """Глубина 0: только корень, без зависимостей."""
    repository = {"A": ["B"], "B": []}
    assert build(repository, "A", 0, NO_FILTER) == {"A": []}


def test_depth_one() -> None:
    """Глубина 1: корень и его прямые зависимости."""
    repository = {"A": ["B"], "B": ["C"], "C": []}
    result = build(repository, "A", 1, NO_FILTER)
    assert result == {"A": ["B"], "B": []}


def test_filter() -> None:
    """Пакеты с подстрокой в имени не учитываются."""
    repository = {"A": ["B", "C"], "B": [], "C": []}
    result = build(repository, "A", BIG_DEPTH, "C")
    assert result == {"A": ["B"], "B": []}


def test_filtered_root() -> None:
    """Если корень отфильтрован, будет ошибка."""
    with pytest.raises(ToolError):
        build({"A": []}, "A", BIG_DEPTH, "A")


def test_unknown_package() -> None:
    """Неизвестный пакет даёт ошибку."""
    with pytest.raises(ToolError):
        build({"A": []}, "Z", BIG_DEPTH, NO_FILTER)


def test_parse_text() -> None:
    """Разбор тестового файла."""
    repository = parse_repository_text("A: B C\nB:\n")
    assert repository == {"A": ["B", "C"], "B": []}


def test_parse_bad_name() -> None:
    """Маленькие буквы в тестовом файле запрещены."""
    with pytest.raises(ToolError):
        parse_repository_text("a: B\n")
