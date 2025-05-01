import pytest

from direction import Direction

@pytest.mark.parametrize("direction, expected_code", [
    (Direction.LEFT, 'Direction.LEFT'),
    (Direction.STAY, 'Direction.STAY'),
    (Direction.RIGHT, 'Direction.RIGHT')
])
def test_code_representation(direction: Direction, expected_code: str) -> None:
    assert direction.to_code() == expected_code

@pytest.mark.parametrize("direction, expected_str", [
    (Direction.LEFT, '-'),
    (Direction.STAY, '0'),
    (Direction.RIGHT, '+')
])
def test_string_representation(direction: Direction, expected_str: str) -> None:
    assert str(direction) == expected_str