import pytest

from tape import Tape
from direction import Direction

@pytest.fixture
def tape() -> Tape:
    return Tape()

def test_defaults(tape: Tape) -> None:
    assert tape.head == 0
    assert tape.read() == "B"

def test_overwrite(tape: Tape) -> None:
    tape.overwrite([1, "A", 2], 3)

    assert tape.content[3] == 1
    assert tape.content[4] == "A"
    assert tape.content[5] == 2

def test_shift(tape: Tape) -> None:
    tape.shift(Direction.RIGHT)
    assert tape.head == 1

    tape.shift(Direction.LEFT)
    assert tape.head == 0

    tape.shift(Direction.LEFT)
    assert tape.head == -1

    tape.shift(Direction.RIGHT)
    tape.shift(Direction.RIGHT)
    tape.shift(Direction.RIGHT)
    assert tape.head == 2

def test_read(tape: Tape) -> None:
    tape.overwrite(["0", "1", 20], 3)

    assert tape.read() == "B"

    tape.shift(Direction.RIGHT)
    assert tape.read() == "B"

    tape.shift(Direction.RIGHT)
    assert tape.read() == "B"

    tape.shift(Direction.RIGHT)
    assert tape.read() == "0"

    tape.shift(Direction.RIGHT)
    assert tape.read() == "1"

    tape.shift(Direction.RIGHT)
    assert tape.read() == 20

def test_write(tape: Tape) -> None:
    tape.write(1)

    tape.shift(Direction.LEFT)
    tape.write("A")
    
    tape.shift(Direction.RIGHT)
    tape.write("B")

    tape.shift(Direction.RIGHT)
    tape.write(2)

    tape.shift(Direction.RIGHT)
    tape.write(3)

    assert tape.content[-1] == "A"
    assert tape.content[0] == "B"
    assert tape.content[1] == 2
    assert tape.content[2] == 3

def test_manipulation(tape: Tape) -> None:
    tape.write(1)
    tape.shift(Direction.RIGHT)
    tape.write("A")
    tape.shift(Direction.RIGHT)
    tape.write("B")
    tape.shift(Direction.RIGHT)
    tape.write(2)
    tape.shift(Direction.RIGHT)
    tape.write(3)
    tape.shift(Direction.RIGHT)

    assert tape.read() == "B"

    tape.shift(Direction.LEFT)
    assert tape.read() == 3
    
    tape.shift(Direction.LEFT)
    assert tape.read() == 2
    
    tape.shift(Direction.LEFT)
    assert tape.read() == "B"
    
    tape.shift(Direction.LEFT)
    assert tape.read() == "A"
    
    tape.shift(Direction.LEFT)
    assert tape.read() == 1
