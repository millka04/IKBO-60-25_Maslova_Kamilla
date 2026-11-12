"""Создание текста диаграммы Mermaid и сохранение картинки PNG."""

import subprocess

from errors import ToolError

HEADER: str = "graph TD"
INDENT: str = "    "
SUCCESS_CODE: int = 0


def make_node_ids(graph: dict[str, list[str]]) -> dict[str, str]:
    """Даёт каждому пакету короткий номер n0, n1, ..."""
    ids: dict[str, str] = {}
    for name in graph:
        ids[name] = "n" + str(len(ids))
    return ids


def make_mermaid_text(graph: dict[str, list[str]]) -> str:
    """Строит текст диаграммы Mermaid по графу."""
    ids: dict[str, str] = make_node_ids(graph)
    lines: list[str] = [HEADER]
    for name, node_id in ids.items():
        lines.append(f'{INDENT}{node_id}["{name}"]')
    for name, dependencies in graph.items():
        for dependency in dependencies:
            lines.append(f"{INDENT}{ids[name]} --> {ids[dependency]}")
    return "\n".join(lines) + "\n"


def save_text(text: str, path: str) -> None:
    """Сохраняет текст в файл."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def render_png(mermaid_path: str, png_path: str) -> None:
    """Превращает файл Mermaid в картинку PNG программой mmdc."""
    command: list[str] = ["mmdc", "-i", mermaid_path, "-o", png_path]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise ToolError("Не найдена программа mmdc (mermaid-cli)") from error
    if result.returncode != SUCCESS_CODE:
        raise ToolError("Ошибка mmdc: " + result.stderr)
