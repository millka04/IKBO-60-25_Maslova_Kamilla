"""Тесты чтения конфигурации."""

from pathlib import Path

import pytest

from config import load_config
from errors import ToolError

EXPECTED_DEPTH: int = 3
GOOD_TEXT: str = (
    "package: serde_json\n"
    "repository: https://index.crates.io\n"
    "test_mode: false\n"
    "output_file: graph.png\n"
    "max_depth: 3\n"
    "filter: ''\n"
)
BAD_REPLACEMENTS: list[tuple[str, str]] = [
    ("max_depth: 3", "max_depth: -1"),
    ("max_depth: 3", "max_depth: abc"),
    ("max_depth: 3", "max_depth: true"),
    ("test_mode: false", "test_mode: maybe"),
    ("output_file: graph.png", "output_file: graph.txt"),
    ("repository: https://index.crates.io", "repository: ftp://site"),
    ("package: serde_json", "package: 'bad name!'"),
    ("filter: ''", "filter: 5"),
]


def write_config(folder: Path, text: str) -> str:
    """Записывает текст в файл конфигурации и возвращает путь."""
    path: Path = folder / "config.yaml"
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_good_config(tmp_path: Path) -> None:
    """Правильный файл читается без ошибок."""
    config = load_config(write_config(tmp_path, GOOD_TEXT))
    assert config["package"] == "serde_json"
    assert config["max_depth"] == EXPECTED_DEPTH


def test_missing_file() -> None:
    """Несуществующий файл даёт понятную ошибку."""
    with pytest.raises(ToolError):
        load_config("no_such_file.yaml")


def test_missing_key(tmp_path: Path) -> None:
    """Отсутствие параметра даёт ошибку."""
    text: str = GOOD_TEXT.replace("max_depth: 3\n", "")
    with pytest.raises(ToolError):
        load_config(write_config(tmp_path, text))


@pytest.mark.parametrize("old, new", BAD_REPLACEMENTS)
def test_bad_values(tmp_path: Path, old: str, new: str) -> None:
    """Каждое неверное значение даёт ошибку (один тест на пару)."""
    text: str = GOOD_TEXT.replace(old, new)
    with pytest.raises(ToolError):
        load_config(write_config(tmp_path, text))
