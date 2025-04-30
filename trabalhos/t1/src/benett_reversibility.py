from direction import Direction
from quintuple_turing_machine import QuintupleTuringMachineDefinition
from quadruple_turing_machine import QuadrupleAct, QuadrupleTransition, QuadrupleTuringMachineDefinition

def is_machine_reversible(quintuple_machine_definition: QuintupleTuringMachineDefinition) -> bool:
    return True

def create_reversible_machine(quintuple_machine_definition: QuintupleTuringMachineDefinition):
    if not is_machine_reversible(quintuple_machine_definition):
        raise ValueError("The machine is not reversible")
    
    quadruple_machine_definition = QuadrupleTuringMachineDefinition(
        tapes=3,
        alphabet=[],
        transitions=[],
        initial_state=f"A{quintuple_machine_definition.initial_state}",
        final_states=[f"C{quintuple_machine_definition.initial_state}"]
    )

    m = 1

    for quintuple_transition in quintuple_machine_definition.transitions:
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f"A{quintuple_transition.source_state}",
                destination_state=f"A'{m}",
                acts=[
                    QuadrupleAct.read_write(quintuple_transition.acts[0].read, quintuple_transition.acts[0].write),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write("B", "B"),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f"A'{m}",
                destination_state=f"A{quintuple_transition.destination_state}",
                acts=[
                    QuadrupleAct.shift(quintuple_transition.acts[0].direction),
                    QuadrupleAct.read_write("B", m),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f"C{quintuple_transition.destination_state}",
                destination_state=f"C'{m}",
                acts=[
                    QuadrupleAct.shift(Direction(-quintuple_transition.acts[0].direction.value)),
                    QuadrupleAct.read_write(m, "B"),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f"C'{m}",
                destination_state=f"C{quintuple_transition.source_state}",
                acts=[
                    QuadrupleAct.read_write(quintuple_transition.acts[0].write, quintuple_transition.acts[0].read),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write("B", "B"),
                ]
            )
        )

        m += 1

    # B states (copy output)
    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state=f"A{quintuple_machine_definition.final_states[0]}",
            destination_state="B'1",
            acts=[
                QuadrupleAct.read_write("B", "B"),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.read_write("B", "B"),
            ]
        )
    )

    for tape_symbol in quintuple_machine_definition.alphabet:
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="B1",
                destination_state=("B'1" if tape_symbol != "B" else "B'2"),
                acts=[
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("B", tape_symbol),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state="B2",
                destination_state=("B'2" if tape_symbol != "B" else f"C{quintuple_machine_definition.final_states[0]}"),
                acts=[
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                ]
            )
        )

    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state="B'1",
            destination_state="B1",
            acts=[
                QuadrupleAct.shift(Direction.RIGHT),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.shift(Direction.RIGHT),
            ]
        )
    )

    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state="B'2",
            destination_state="B2",
            acts=[
                QuadrupleAct.shift(Direction.LEFT),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.shift(Direction.LEFT),
            ]
        )
    )

    return quadruple_machine_definition