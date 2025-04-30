import pytest
from typing import Any

from mark import format_mark_for_display, format_mark_for_code

@pytest.mark.parametrize("mark, expected_str", [
    (0, "#0"),
    (1, "#1"),
    (100, "#100"),
    (-1, "#-1"),
    (-100, "#-100"),
    (1234567890, "#1234567890"),
    (9999999999, "#9999999999")
])
def test_format_for_display_with_int(mark: Any, expected_str: str) -> None:
    assert format_mark_for_display(mark) == expected_str

@pytest.mark.parametrize("mark, expected_str", [
    ("", ""),
    ("A", "A"),
    ("ABC", "ABC")
])
def test_format_for_display_with_string(mark: Any, expected_str: str) -> None:
    assert format_mark_for_display(mark) == expected_str

@pytest.mark.parametrize("mark", [
    [],
    {},
    set(),
    tuple(),
    object()
])
def test_format_for_display_with_unsupported_type(mark: Any) -> None:
    with pytest.raises(ValueError):
        format_mark_for_display(mark)

@pytest.mark.parametrize("mark, expected_str", [
    (0, "0"),
    (1, "1"),
    (100, "100"),
    (-1, "-1"),
    (-100, "-100"),
    (1234567890, "1234567890"),
    (9999999999, "9999999999")
])
def test_format_for_code_with_int(mark: Any, expected_str: str) -> None:
    assert format_mark_for_code(mark) == expected_str

@pytest.mark.parametrize("mark, expected_str", [
    ('', "''"),
    ('A', "'A'"),
    ('ABC', "'ABC'"),
    ("'", "'\\''")
])
def test_format_for_code_with_string(mark: Any, expected_str: str) -> None:
    assert format_mark_for_code(mark) == expected_str

@pytest.mark.parametrize("mark", [
    [],
    {},
    set(),
    tuple(),
    object()
])
def test_format_for_code_with_unsupported_type(mark: Any) -> None:
    with pytest.raises(ValueError):
        format_mark_for_code(mark)
