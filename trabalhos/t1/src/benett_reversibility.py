from direction import Direction
from quintuple_turing_machine import QuintupleAct, QuintupleTuringMachineDefinition
from quadruple_turing_machine import QuadrupleAct, QuadrupleTransition, QuadrupleTuringMachineDefinition

def is_machine_reversible(quintuple_machine_definition: QuintupleTuringMachineDefinition) -> bool:
    if quintuple_machine_definition.tapes != 1:
        return False

    initial_state = quintuple_machine_definition.initial_state
    final_state = quintuple_machine_definition.final_states[0]

    transitions = quintuple_machine_definition.transitions

    for transition in transitions:
        if len(transition.acts) != 1:
            return False

    transitions_from_initial_state = list(filter(lambda t: t.source_state == initial_state, transitions))
    transitions_to_initial_state = list(filter(lambda t: t.destination_state == initial_state, transitions))

    transitions_from_final_state = list(filter(lambda t: t.source_state == final_state, transitions))
    transitions_to_final_state = list(filter(lambda t: t.destination_state == final_state, transitions))

    required_initial_act = QuintupleAct('B', 'B', Direction.RIGHT)
    required_final_act = QuintupleAct('B', 'B', Direction.STAY)

    if len(transitions_from_initial_state) != 1:
        return False
    
    if len(transitions_to_initial_state) != 0:
        return False
    
    if len(transitions_from_final_state) != 0:
        return False
    
    if len(transitions_to_final_state) != 1:
        return False
    
    if transitions_from_initial_state[0].acts[0] != required_initial_act:
        return False   
    
    if transitions_to_final_state[0].acts[0] != required_final_act:
        return False
    
    return True
    
def create_reversible_machine(quintuple_machine_definition: QuintupleTuringMachineDefinition):
    if not is_machine_reversible(quintuple_machine_definition):
        raise ValueError('The machine is not reversible')
    
    quadruple_machine_definition = QuadrupleTuringMachineDefinition(
        tapes=3,
        alphabet=quintuple_machine_definition.alphabet + list(range(1, len(quintuple_machine_definition.transitions) + 1)),
        transitions=[],
        initial_state=f'A{quintuple_machine_definition.initial_state}',
        final_states=[f'C{quintuple_machine_definition.initial_state}']
    )

    m = 1

    for quintuple_transition in quintuple_machine_definition.transitions:
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f'A{quintuple_transition.source_state}',
                destination_state=f"A'{m}",
                acts=[
                    QuadrupleAct.read_write(quintuple_transition.acts[0].read, quintuple_transition.acts[0].write),
                    QuadrupleAct.shift(Direction.RIGHT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f"A'{m}",
                destination_state=f'A{quintuple_transition.destination_state}',
                acts=[
                    QuadrupleAct.shift(quintuple_transition.acts[0].direction),
                    QuadrupleAct.read_write('B', m),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f'C{quintuple_transition.destination_state}',
                destination_state=f"C'{m}",
                acts=[
                    QuadrupleAct.shift(Direction(-quintuple_transition.acts[0].direction.value)),
                    QuadrupleAct.read_write(m, 'B'),
                    QuadrupleAct.shift(Direction.STAY),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state=f"C'{m}",
                destination_state=f'C{quintuple_transition.source_state}',
                acts=[
                    QuadrupleAct.read_write(quintuple_transition.acts[0].write, quintuple_transition.acts[0].read),
                    QuadrupleAct.shift(Direction.LEFT),
                    QuadrupleAct.read_write('B', 'B'),
                ]
            )
        )

        m += 1

    # B states (copy output)
    quadruple_machine_definition.transitions.append(
        QuadrupleTransition(
            source_state=f'A{quintuple_machine_definition.final_states[0]}',
            destination_state="B'1",
            acts=[
                QuadrupleAct.read_write('B', 'B'),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.read_write('B', 'B'),
            ]
        )
    )

    for tape_symbol in quintuple_machine_definition.alphabet:
        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state='B1',
                destination_state=("B'1" if tape_symbol != 'B' else "B'2"),
                acts=[
                    QuadrupleAct.read_write(tape_symbol, tape_symbol),
                    QuadrupleAct.shift(Direction.STAY),
                    QuadrupleAct.read_write("B", tape_symbol),
                ]
            )
        )

        quadruple_machine_definition.transitions.append(
            QuadrupleTransition(
                source_state='B2',
                destination_state=("B'2" if tape_symbol != 'B' else f'C{quintuple_machine_definition.final_states[0]}'),
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
            destination_state='B1',
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
            destination_state='B2',
            acts=[
                QuadrupleAct.shift(Direction.LEFT),
                QuadrupleAct.shift(Direction.STAY),
                QuadrupleAct.shift(Direction.LEFT),
            ]
        )
    )

    return quadruple_machine_definition