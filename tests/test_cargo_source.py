"""Тесты получения зависимостей Cargo."""

import pytest

from cargo_source import (
    find_latest_version,
    get_normal_dependencies,
    make_index_path,
)
from errors import ToolError

INDEX_TEXT: str = (
    '{"name":"demo","vers":"1.0.0","yanked":false,"deps":[]}\n'
    '{"name":"demo","vers":"1.1.0","yanked":false,"deps":['
    '{"name":"a","kind":"normal","optional":false},'
    '{"name":"b","kind":"dev","optional":false},'
    '{"name":"c","kind":"normal","optional":true},'
    '{"name":"x","package":"d","kind":"normal","optional":false}]}\n'
    '{"name":"demo","vers":"2.0.0-beta","yanked":false,"deps":[]}\n'
    '{"name":"demo","vers":"1.2.0","yanked":true,"deps":[]}\n'
)
PATH_CASES: list[tuple[str, str]] = [
    ("a", "1/a"),
    ("ab", "2/ab"),
    ("abc", "3/a/abc"),
    ("serde", "se/rd/serde"),
]


@pytest.mark.parametrize("name, expected", PATH_CASES)
def test_make_index_path(name: str, expected: str) -> None:
    """Путь к файлу пакета строится по правилам индекса."""
    assert make_index_path(name) == expected


def test_latest_version() -> None:
    """Берётся последняя версия без отзыва и без пре-релиза."""
    info = find_latest_version(INDEX_TEXT)
    assert info["vers"] == "1.1.0"


def test_normal_dependencies() -> None:
    """Dev, опциональные отбрасываются, переименование учитывается."""
    info = find_latest_version(INDEX_TEXT)
    assert get_normal_dependencies(info) == ["a", "d"]


def test_no_version() -> None:
    """Пустой индекс даёт ошибку."""
    with pytest.raises(ToolError):
        find_latest_version("")
