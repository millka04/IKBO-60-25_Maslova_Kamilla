"""Обратные зависимости: какие пакеты зависят от заданного."""

from errors import ToolError
from graph import GraphBuilder
from sources import DictSource


def reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Разворачивает рёбра: вместо 'A зависит от B' получаем 'B для A'."""
    reversed_graph: dict[str, list[str]] = {}
    for name in graph:
        reversed_graph[name] = []
    for name, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in reversed_graph:
                reversed_graph[dependency] = []
            reversed_graph[dependency].append(name)
    return reversed_graph


def find_reverse_dependencies(
    graph: dict[str, list[str]], target: str
) -> list[str]:
    """Возвращает пакеты, которые зависят от target прямо или через цепочку."""
    if target not in graph:
        raise ToolError(f"Пакет {target} не найден в графе")
    source = DictSource(reverse_graph(graph))
    builder = GraphBuilder(source, len(graph), "")
    result: dict[str, list[str]] = builder.build(target)
    names: list[str] = []
    for name in result:
        if name != target:
            names.append(name)
    return names
