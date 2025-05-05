import pytest
from typing import List, Dict, Any

from quadruple_turing_machine import QuadrupleTransition, QuadrupleAct, QuadrupleTuringMachineDefinition, QuadrupleTuringMachineSimulator
from direction import Direction

@pytest.fixture
def definition():
    return QuadrupleTuringMachineDefinition(
        tapes=2,
        alphabet=["0", "1"],
        transitions=[
            QuadrupleTransition(
                source_state="1",
                destination_state="2",
                acts=[
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("0", "0")
                ]
            ),
            QuadrupleTransition(
                source_state="1",
                destination_state="2",
                acts=[
                    QuadrupleAct.read_write("0", "1"),
                    QuadrupleAct.read_write("1", "1")
                ]
            ),
            QuadrupleTransition(
                source_state="1",
                destination_state="2",
                acts=[
                    QuadrupleAct.read_write("1", "0"),
                    QuadrupleAct.read_write("1", "1")
                ]
            ),
            QuadrupleTransition(
                source_state="1",
                destination_state="3",
                acts=[
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("B", "B")
                ]
            ),
            QuadrupleTransition(
                source_state="2",
                destination_state="1",
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.shift(Direction.RIGHT)
                ]
            ),
            QuadrupleTransition(
                source_state="3",
                destination_state="4",
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.shift(Direction.LEFT)
                ]
            ),
        ],
        initial_state="1",
        final_states=["4"]
    )

@pytest.mark.parametrize("current_state, data, expected_result", [
    ("0", ["a", "0", 0], True),
    ("0", ["a", "1", 0], True),
    ("1", ["a", "0", 0], False),
    ("1", ["a", "1", 0], False),
    ("0", ["b", "0", 0], False),
    ("0", ["a", "0", "0"], False)
])
def test_transition_matching(current_state: str, data: List[Any], expected_result: bool) -> None:
    transition = QuadrupleTransition(
        source_state="0",
        destination_state="1",
        acts=[
            QuadrupleAct.read_write("a", "b"),
            QuadrupleAct.shift(Direction.RIGHT),
            QuadrupleAct.read_write(0, 1),
        ]
    )

    assert transition.matches(current_state, data) == expected_result

def test_transition_string_representation():
    transition = QuadrupleTransition(
        source_state="q0",
        destination_state="q1",
        acts=[
            QuadrupleAct.read_write("a", "b"),
            QuadrupleAct.shift(Direction.RIGHT),
            QuadrupleAct.read_write(0, "1"),
        ]
    )

    assert str(transition) == "q0[a / #0] -> [b + 1]q1"

@pytest.mark.parametrize("act, expected_code", [
    (QuadrupleAct.read_write("a", "b"), "QuadrupleAct.read_write('a', 'b')"),
    (QuadrupleAct.shift(Direction.RIGHT), 'QuadrupleAct.shift(Direction.RIGHT)'),
    (QuadrupleAct.read_write(0, "1"), "QuadrupleAct.read_write(0, '1')"),
])
def test_act_code_representation(act: QuadrupleAct, expected_code: str) -> None:
    assert act.to_code() == expected_code

def test_transition_code_representation():
    transition = QuadrupleTransition(
        source_state="q0",
        destination_state="q1",
        acts=[
            QuadrupleAct.read_write("a", "b"),
            QuadrupleAct.shift(Direction.RIGHT),
            QuadrupleAct.read_write(0, "1"),
        ]
    )

    assert transition.to_code() == (
        "QuadrupleTransition(\n"
        "    source_state='q0',\n"
        "    destination_state='q1',\n"
        "    acts=[\n"
        "        QuadrupleAct.read_write('a', 'b'),\n"
        "        QuadrupleAct.shift(Direction.RIGHT),\n"
        "        QuadrupleAct.read_write(0, '1'),\n"
        "    ]\n"
        ")"
    )

@pytest.mark.parametrize("current_state, data, expected_transition", [
    (
        "1",
        ["0", "1"],
        QuadrupleTransition(
            source_state="1",
            destination_state="2",
            acts=[
                QuadrupleAct.read_write("0", "1"),
                QuadrupleAct.read_write("1", "1")
            ]
        )
    ),
    (
        "1",
        ["B", "B"],
        QuadrupleTransition(
            source_state="1",
            destination_state="3",
            acts=[
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.read_write("B", "B")
            ]
        )
    ),
    (
        "3",
        ["0", "0"],
        QuadrupleTransition(
            source_state="3",
            destination_state="4",
            acts=[
                QuadrupleAct.shift(Direction.LEFT),
                QuadrupleAct.shift(Direction.LEFT)
            ]
        )
    ),
    (
        "1",
        ["X", "1"],
        None
    )
])
def test_definition_transition_matching(
    definition: QuadrupleTuringMachineDefinition,
    current_state: str,
    data: List[Any],
    expected_transition: QuadrupleTransition) -> None:

    assert definition.find_matching_transition(current_state, data) == expected_transition

def test_definition_code_representation(definition: QuadrupleTuringMachineDefinition) -> None:
    assert definition.to_code() == (
        "QuadrupleTuringMachineDefinition(\n"
        "    tapes=2,\n"
        "    alphabet=['0', '1'],\n"
        "    transitions=[\n"
        "        QuadrupleTransition(\n"
        "            source_state='1',\n"
        "            destination_state='2',\n"
        "            acts=[\n"
        "                QuadrupleAct.shift(Direction.STAY),\n"
        "                QuadrupleAct.read_write('0', '0'),\n"
        "            ]\n"
        "        ),\n"
        "        QuadrupleTransition(\n"
        "            source_state='1',\n"
        "            destination_state='2',\n"
        "            acts=[\n"
        "                QuadrupleAct.read_write('0', '1'),\n"
        "                QuadrupleAct.read_write('1', '1'),\n"
        "            ]\n"
        "        ),\n"
        "        QuadrupleTransition(\n"
        "            source_state='1',\n"
        "            destination_state='2',\n"
        "            acts=[\n"
        "                QuadrupleAct.read_write('1', '0'),\n"
        "                QuadrupleAct.read_write('1', '1'),\n"
        "            ]\n"
        "        ),\n"
        "        QuadrupleTransition(\n"
        "            source_state='1',\n"
        "            destination_state='3',\n"
        "            acts=[\n"
        "                QuadrupleAct.shift(Direction.STAY),\n"
        "                QuadrupleAct.read_write('B', 'B'),\n"
        "            ]\n"
        "        ),\n"
        "        QuadrupleTransition(\n"
        "            source_state='2',\n"
        "            destination_state='1',\n"
        "            acts=[\n"
        "                QuadrupleAct.shift(Direction.RIGHT),\n"
        "                QuadrupleAct.shift(Direction.RIGHT),\n"
        "            ]\n"
        "        ),\n"
        "        QuadrupleTransition(\n"
        "            source_state='3',\n"
        "            destination_state='4',\n"
        "            acts=[\n"
        "                QuadrupleAct.shift(Direction.LEFT),\n"
        "                QuadrupleAct.shift(Direction.LEFT),\n"
        "            ]\n"
        "        ),\n"
        "    ],\n"
        "    initial_state='1',\n"
        "    final_states=['4']\n"
        ")"
    )

def test_definition_equality(definition: QuadrupleTuringMachineDefinition) -> None:
    definition2 = QuadrupleTuringMachineDefinition(
        tapes=2,
        alphabet=["1", "0"],
        transitions=[
            QuadrupleTransition(
                source_state="1",
                destination_state="2",
                acts=[
                    QuadrupleAct.read_write("0", "1"),
                    QuadrupleAct.read_write("1", "1")
                ]
            ),
            QuadrupleTransition(
                source_state="1",
                destination_state="2",
                acts=[
                    QuadrupleAct.read_write("1", "0"),
                    QuadrupleAct.read_write("1", "1")
                ]
            ),
            QuadrupleTransition(
                source_state="1",
                destination_state="2",
                acts=[
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("0", "0")
                ]
            ),
            QuadrupleTransition(
                source_state="1",
                destination_state="3",
                acts=[
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("B", "B")
                ]
            ),
            QuadrupleTransition(
                source_state="2",
                destination_state="1",
                acts=[
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.shift(Direction.RIGHT)
                ]
            ),
            QuadrupleTransition(
                source_state="3",
                destination_state="4",
                acts=[
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.shift(Direction.LEFT)
                ]
            ),
        ],
        initial_state="1",
        final_states=["4"]
    )

    assert definition == definition2
    
@pytest.mark.parametrize("transitions, inputs, outputs, heads, final_state, accepted, rejected, halted", [
    (
        [0, 4, 2, 4, 0, 4, 1, 4, 3, 5, None],
        [
            {0: "0", 1: "1", 2: "1", 3: "0"},
            {0: "0", 1: "1", 2: "0", 3: "1"}
        ] ,
        [
            {0: "0", 1: "0", 2: "1", 3: "1"},
            {0: "0", 1: "1", 2: "0", 3: "1"}
        ],
        [3, 3],
        "4",
        True,
        False,
        True
    ),
    (
        [0, 4, 2, 4],
        [
            {0: "0", 1: "1", 2: "1", 3: "0"},
            {0: "0", 1: "1", 2: "0", 3: "1"}
        ],
        [
            {0: "0", 1: "0", 2: "1", 3: "0"},
            {0: "0", 1: "1", 2: "0", 3: "1"}
        ],
        [2, 2],
        "1",
        False,
        False,
        False
    ),
    (
        [0, 4, None],
        [
            {0: "0", 1: "X", 2: "1", 3: "0"},
            {0: "0", 1: "1", 2: "0", 3: "1"}
        ],
        [
            {0: "0", 1: "X", 2: "1", 3: "0"},
            {0: "0", 1: "1", 2: "0", 3: "1"}
        ],
        [1, 1],
        "1",
        False,
        True,
        True
    )
])
def test_simulator_execution(
    definition: QuadrupleTuringMachineDefinition,
    transitions: List[int],
    inputs: List[Dict[int, Any]],
    outputs: List[Dict[int, Any]],
    heads: List[int],
    final_state: str,
    accepted: bool,
    rejected: bool,
    halted: bool) -> None:
    simulator = QuadrupleTuringMachineSimulator(definition)

    for i, content in enumerate(inputs):
        simulator.tapes[i].content = content
    
    assert simulator.current_state == definition.initial_state

    for i, expected_transition in enumerate(transitions):
        if expected_transition == None:
            assert simulator.step() == None
        else:
            assert simulator.step() == definition.transitions[expected_transition]
    
    assert simulator.current_state == final_state

    assert simulator.has_accepted() == accepted
    assert simulator.has_rejected() == rejected
    assert simulator.has_halted() == halted

    for i, content in enumerate(outputs):
        for j, mark in content.items():
            assert simulator.tapes[i].content[j] == mark
    
    for i, head in enumerate(heads):
        assert simulator.tapes[i].head == head
