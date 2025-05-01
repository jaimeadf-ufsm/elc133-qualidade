import pytest

from direction import Direction
from quintuple_turing_machine import QuintupleAct, QuintupleTransition, QuintupleTuringMachineDefinition
from quadruple_turing_machine import QuadrupleAct, QuadrupleTransition, QuadrupleTuringMachineDefinition
from benett_reversibility import is_machine_reversible, create_reversible_machine

def test_reversibility_check_with_valid_machine():
    machine = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            )
        ],
        initial_state='1',
        final_states=['3']
    )

    assert is_machine_reversible(machine) == True

def test_reversibility_check_with_multiple_tapes():
    machine = QuintupleTuringMachineDefinition(
        tapes=2,
        alphabet=['B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT),
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY),
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            )
        ],
        initial_state='1',
        final_states=['3']
    )

    assert is_machine_reversible(machine) == False

def test_reversibility_check_with_single_incoming_initial_transition():
    machine = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            ),
            QuintupleTransition(
                source_state='4',
                destination_state='1',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            )
        ],
        initial_state='1',
        final_states=['3']
    )

    assert is_machine_reversible(machine) == False

def test_reversibility_check_with_multiple_outgoing_initial_transitions():
    machine = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            ),
            QuintupleTransition(
                source_state='1',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            )
        ],
        initial_state='1',
        final_states=['3']
    )

    assert is_machine_reversible(machine) == False

def test_reversibility_check_with_multiple_incoming_final_transitions():
    machine = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='4',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='4',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            )
        ],
        initial_state='1',
        final_states=['4']
    )

    assert is_machine_reversible(machine) == False

def test_reversibility_check_with_single_outgoing_final_transition():
    machine = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT)
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='4',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY)
                ]
            )
        ],
        initial_state='1',
        final_states=['3']
    )

    assert is_machine_reversible(machine) == False

def test_reversibile_machine_creation():
    quintuple_machine = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['0', '1', 'B'],
        transitions=[
            QuintupleTransition(
                source_state='1',
                destination_state='2',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='2',
                acts=[
                    QuintupleAct('0', '1', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='2',
                acts=[
                    QuintupleAct('1', '0', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='3',
                acts=[
                    QuintupleAct('B', 'B', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='3',
                acts=[
                    QuintupleAct('0', '0', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='3',
                acts=[
                    QuintupleAct('1', '1', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='4',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY),
                ]
            ),
        ],
        initial_state='1',
        final_states=['4']
    )

    expected_reversible_machine = QuadrupleTuringMachineDefinition(
        tapes=3,
        alphabet=['0', '1', 'B', 1, 2, 3, 4, 5, 6, 7],
        transitions=[
            QuadrupleTransition(
                source_state='A1',
                destination_state='A\'1',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'1',
                destination_state='A2',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 1),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C2',
                destination_state='C\'1',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write(1, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'1',
                destination_state='C1',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A2',
                destination_state='A\'2',
                acts=[
                    QuadrupleAct.read_write('0', '1'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'2',
                destination_state='A2',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 2),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C2',
                destination_state='C\'2',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write(2, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'2',
                destination_state='C2',
                acts=[
                    QuadrupleAct.read_write('1', '0'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A2',
                destination_state='A\'3',
                acts=[
                    QuadrupleAct.read_write('1', '0'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'3',
                destination_state='A2',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 3),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C2',
                destination_state='C\'3',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write(3, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'3',
                destination_state='C2',
                acts=[
                    QuadrupleAct.read_write('0', '1'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A2',
                destination_state='A\'4',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'4',
                destination_state='A3',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 4),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C3',
                destination_state='C\'4',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write(4, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'4',
                destination_state='C2',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A3',
                destination_state='A\'5',
                acts=[
                    QuadrupleAct.read_write('0', '0'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'5',
                destination_state='A3',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 5),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C3',
                destination_state='C\'5',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write(5, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'5',
                destination_state='C3',
                acts=[
                    QuadrupleAct.read_write('0', '0'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A3',
                destination_state='A\'6',
                acts=[
                    QuadrupleAct.read_write('1', '1'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'6',
                destination_state='A3',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 6),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C3',
                destination_state='C\'6',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write(6, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'6',
                destination_state='C3',
                acts=[
                    QuadrupleAct.read_write('1', '1'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A3',
                destination_state='A\'7',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A\'7',
                destination_state='A4',
                acts=[
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('B', 7),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C4',
                destination_state='C\'7',
                acts=[
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write(7, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            ),
            QuadrupleTransition(
                source_state='C\'7',
                destination_state='C3',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='A4',
                destination_state='B\'1',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='B1',
                destination_state='B\'1',
                acts=[
                    QuadrupleAct.read_write('0', '0'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('B', '0'),
                ]
            ),
            QuadrupleTransition(
                source_state='B2',
                destination_state='B\'2',
                acts=[
                    QuadrupleAct.read_write('0', '0'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('0', '0'),
                ]
            ),
            QuadrupleTransition(
                source_state='B1',
                destination_state='B\'1',
                acts=[
                    QuadrupleAct.read_write('1', '1'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('B', '1'),
                ]
            ),
            QuadrupleTransition(
                source_state='B2',
                destination_state='B\'2',
                acts=[
                    QuadrupleAct.read_write('1', '1'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('1', '1'),
                ]
            ),
            QuadrupleTransition(
                source_state='B1',
                destination_state='B\'2',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='B2',
                destination_state='C4',
                acts=[
                    QuadrupleAct.read_write('B', 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            ),
            QuadrupleTransition(
                source_state='B\'1',
                destination_state='B1',
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.shift(Direction.RIGHT),
                ]
            ),
            QuadrupleTransition(
                source_state='B\'2',
                destination_state='B2',
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.shift(Direction.LEFT),
                ]
            ),
        ],
        initial_state='A1',
        final_states=['C1']
    )

    assert create_reversible_machine(quintuple_machine) == expected_reversible_machine