import pytest

from state import format_state_for_code

@pytest.mark.parametrize("state, expected_code", [
    ("q0", "'q0'"),
    ("q1", "'q1'"),
    ("q2", "'q2'"),
    ("state_with_space", "'state_with_space'"),
    ("state_with_special_char_!@#$%^&*'", "'state_with_special_char_!@#$%^&*\\''")
])
def test_format_state_for_code(state: str, expected_code: str) -> None:
    assert format_state_for_code(state) == expected_code