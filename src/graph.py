"""Построение графа зависимостей обходом в глубину."""

from errors import ToolError
from sources import DependencySource

ROOT_DEPTH: int = 0


class GraphBuilder:
    """Строит граф зависимостей рекурсивным обходом в глубину."""

    def __init__(
        self, source: DependencySource, max_depth: int, substring: str
    ) -> None:
        self.source: DependencySource = source
        self.max_depth: int = max_depth
        self.substring: str = substring
        self.graph: dict[str, list[str]] = {}
        self.depth_of: dict[str, int] = {}

    def is_filtered(self, name: str) -> bool:
        """Проверяет, нужно ли пропустить пакет из-за фильтра."""
        if not self.substring:
            return False
        return self.substring in name

    def visit(self, name: str, depth: int) -> None:
        """Обходит пакет и рекурсивно его зависимости."""
        if name in self.depth_of and self.depth_of[name] <= depth:
            return
        self.depth_of[name] = depth
        if depth >= self.max_depth:
            self.graph[name] = []
            return
        dependencies: list[str] = []
        for dependency in self.source.get_dependencies(name):
            if not self.is_filtered(dependency):
                dependencies.append(dependency)
        self.graph[name] = dependencies
        for dependency in dependencies:
            self.visit(dependency, depth + 1)

    def build(self, root: str) -> dict[str, list[str]]:
        """Строит граф для корневого пакета."""
        if self.is_filtered(root):
            raise ToolError(f"Пакет {root} исключён фильтром")
        self.visit(root, ROOT_DEPTH)
        return self.graph
