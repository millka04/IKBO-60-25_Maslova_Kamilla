"""Тесты создания текста Mermaid."""

from mermaid import make_mermaid_text


def test_mermaid_text() -> None:
    """Узлы и рёбра попадают в текст диаграммы."""
    graph = {"A": ["B"], "B": []}
    text: str = make_mermaid_text(graph)
    assert text.startswith("graph TD")
    assert 'n0["A"]' in text
    assert "n0 --> n1" in text
