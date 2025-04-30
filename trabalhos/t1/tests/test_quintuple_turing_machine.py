import pytest

from io import StringIO

from direction import Direction
from quintuple_turing_machine import QuintupleAct, QuintupleTransition, QuintupleTuringMachineDefinition
    
@pytest.mark.parametrize("act, expected_code", [
    (QuintupleAct('a', 'b', Direction.LEFT), "QuintupleAct('a', 'b', Direction.LEFT)"),
    (QuintupleAct('B', 'B', Direction.STAY), "QuintupleAct('B', 'B', Direction.STAY)"),
    (QuintupleAct(0, '1', Direction.RIGHT), "QuintupleAct(0, '1', Direction.RIGHT)"),
])
def test_act_code_representation(act: QuintupleAct, expected_code: str) -> None:
    assert act.to_code() == expected_code

def test_transition_code_representation() -> None:
    transition = QuintupleTransition(
        source_state="q0",
        destination_state="q1",
        acts=[
            QuintupleAct('a', 'b', Direction.LEFT),
            QuintupleAct('B', 'B', Direction.STAY),
            QuintupleAct(0, '1', Direction.RIGHT),
        ]
    )

    assert transition.to_code() == (
        "QuintupleTransition(\n"
        "    source_state='q0',\n"
        "    destination_state='q1',\n"
        "    acts=[\n"
        "        QuintupleAct('a', 'b', Direction.LEFT),\n"
        "        QuintupleAct('B', 'B', Direction.STAY),\n"
        "        QuintupleAct(0, '1', Direction.RIGHT),\n"
        "    ]\n"
        ")"
    )

@pytest.mark.parametrize("line, expected_transition", [
    (
        '(3,1)=(5,X,L)',
        QuintupleTransition(
            source_state='3',
            destination_state='5',
            acts=[
                QuintupleAct('1', 'X', Direction.LEFT)
            ]
        )
    ),
    (
        '(1,B)=(2,B,R)',
        QuintupleTransition(
            source_state='1',
            destination_state='2',
            acts=[
                QuintupleAct('B', 'B', Direction.RIGHT)
            ]
        )
    ),
    (
        '(7,B)=(8,B,S)',
        QuintupleTransition(
            source_state='7',
            destination_state='8',
            acts=[
                QuintupleAct('B', 'B', Direction.STAY)
            ]
        )
    )
])
def test_transition_parse(line: str, expected_transition: QuintupleTransition) -> None:
    assert QuintupleTransition.parse(line) == expected_transition

def test_definition_parse() -> None:
    stream = StringIO(
        '8 2 5 23\n'
        '1 2 3 4 5 6 7 8\n'
        '0 1 \n'
        '0 1 $ X B\n'
        '(1,B)=(2,B,R)\n'
        '(2,0)=(3,$,R)\n'
        '(2,1)=(4,$,R)\n'
        '(2,B)=(7,B,R)\n'
        '(3,0)=(3,0,R)\n'
        '(3,X)=(3,X,R)\n'
        '(3,1)=(5,X,L)\n'
        '(4,1)=(4,1,R)\n'
        '(4,X)=(4,X,R)\n'
        '(4,0)=(5,X,L)\n'
        '(5,0)=(5,0,L)\n'
        '(5,1)=(5,1,L)\n'
        '(5,X)=(5,X,L)\n'
        '(5,$)=(6,$,R)\n'
        '(6,X)=(6,X,R)\n'
        '(6,0)=(3,X,R)\n'
        '(6,1)=(4,X,R)\n'
        '(6,B)=(7,B,L)\n'
        '(7,0)=(7,0,L)\n'
        '(7,1)=(7,1,L)\n'
        '(7,$)=(7,$,L)\n'
        '(7,X)=(7,X,L)\n'
        '(7,B)=(8,B,S)\n'
    )

    expected_definition = QuintupleTuringMachineDefinition(
        tapes=1,
        alphabet=['0', '1', '$', 'X', 'B'],
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
                destination_state='3',
                acts=[
                    QuintupleAct('0', '$', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='4',
                acts=[
                    QuintupleAct('1', '$', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='2',
                destination_state='7',
                acts=[
                    QuintupleAct('B', 'B', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='3',
                acts=[
                    QuintupleAct('0', '0', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='3',
                acts=[
                    QuintupleAct('X', 'X', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='3',
                destination_state='5',
                acts=[
                    QuintupleAct('1', 'X', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='4',
                destination_state='4',
                acts=[
                    QuintupleAct('1', '1', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='4',
                destination_state='4',
                acts=[
                    QuintupleAct('X', 'X', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='4',
                destination_state='5',
                acts=[
                    QuintupleAct('0', 'X', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='5',
                destination_state='5',
                acts=[
                    QuintupleAct('0', '0', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='5',
                destination_state='5',
                acts=[
                    QuintupleAct('1', '1', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='5',
                destination_state='5',
                acts=[
                    QuintupleAct('X', 'X', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='5',
                destination_state='6',
                acts=[
                    QuintupleAct('$', '$', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='6',
                destination_state='6',
                acts=[
                    QuintupleAct('X', 'X', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='6',
                destination_state='3',
                acts=[
                    QuintupleAct('0', 'X', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='6',
                destination_state='4',
                acts=[
                    QuintupleAct('1', 'X', Direction.RIGHT),
                ]
            ),
            QuintupleTransition(
                source_state='6',
                destination_state='7',
                acts=[
                    QuintupleAct('B', 'B', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='7',
                destination_state='7',
                acts=[
                    QuintupleAct('0', '0', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='7',
                destination_state='7',
                acts=[
                    QuintupleAct('1', '1', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='7',
                destination_state='7',
                acts=[
                    QuintupleAct('$', '$', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='7',
                destination_state='7',
                acts=[
                    QuintupleAct('X', 'X', Direction.LEFT),
                ]
            ),
            QuintupleTransition(
                source_state='7',
                destination_state='8',
                acts=[
                    QuintupleAct('B', 'B', Direction.STAY),
                ]
            )
        ],
        initial_state='1',
        final_states=['8']
    )

    assert QuintupleTuringMachineDefinition.parse(stream) == expected_definition
    

