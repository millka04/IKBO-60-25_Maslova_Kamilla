"""Тесты обратных зависимостей."""

import pytest

from errors import ToolError
from reverse import find_reverse_dependencies, reverse_graph


def test_reverse_graph() -> None:
    """Рёбра разворачиваются."""
    graph = {"A": ["B"], "B": []}
    assert reverse_graph(graph) == {"A": [], "B": ["A"]}


def test_chain() -> None:
    """В цепочке от C зависят B и A."""
    graph = {"A": ["B"], "B": ["C"], "C": []}
    assert find_reverse_dependencies(graph, "C") == ["B", "A"]


def test_cycle() -> None:
    """В цикле нет бесконечной рекурсии."""
    graph = {"A": ["B"], "B": ["A"]}
    assert find_reverse_dependencies(graph, "A") == ["B"]


def test_no_dependents() -> None:
    """От корня никто не зависит."""
    graph = {"A": ["B"], "B": []}
    assert find_reverse_dependencies(graph, "A") == []


def test_unknown_target() -> None:
    """Пакета нет в графе: ошибка."""
    with pytest.raises(ToolError):
        find_reverse_dependencies({"A": []}, "Z")
