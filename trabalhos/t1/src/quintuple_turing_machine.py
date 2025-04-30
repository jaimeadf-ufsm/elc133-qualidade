from typing import Any, Self, List, TextIO
from dataclasses import dataclass
import re

from direction import Direction
from mark import format_mark_for_code

@dataclass
class QuintupleAct:
    read: Any
    write: Any
    direction: Direction

    def to_code(self) -> str:
        return 'QuintupleAct(' \
            f'{format_mark_for_code(self.read)}, ' \
            f'{format_mark_for_code(self.write)}, ' \
            f'{self.direction.to_code()})'

@dataclass
class QuintupleTransition:
    source_state: int
    destination_state: int
    acts: List[QuintupleAct]

    def to_code(self) -> str:
        result = f'QuintupleTransition(\n'
        result += f"    source_state='{self.source_state}',\n"
        result += f"    destination_state='{self.destination_state}',\n"
        result += f"    acts=[\n"

        for act in self.acts:
            result += f"        {act.to_code()},\n"
        
        result += f"    ]\n"
        result += f")"

        return result

    def parse(line: str) -> Self:
        p = re.compile(r'\((?P<source>\d+),(?P<read>.+)\)=\((?P<destination>\d+),(?P<write>.+),(?P<shift>[RLS])\)')
        match = p.match(line)

        if not match:
            raise ValueError(f'Invalid quintuple format: {line}')
        
        source_state = match.group('source')
        read_symbol = match.group('read')
        destination_state = match.group('destination')
        write_symbol = match.group('write')
        shift = match.group('shift')

        direction_lookup = {
            'L': Direction.LEFT,
            'R': Direction.RIGHT,
            'S': Direction.STAY
        }

        return QuintupleTransition(
            source_state=source_state,
            destination_state=destination_state,
            acts=[
                QuintupleAct(
                    read=read_symbol,
                    write=write_symbol,
                    direction=direction_lookup[shift]
                )
            ]
        )
    
@dataclass
class QuintupleTuringMachineDefinition:
    tapes: int
    alphabet: List[Any]
    transitions: List[QuintupleTransition]
    initial_state: str
    final_states: List[str]

    def parse(stream: TextIO) -> Self:
        quintuple_machine_definition = QuintupleTuringMachineDefinition(
            tapes=1,
            alphabet=[],
            transitions=[],
            initial_state='',
            final_states=[]
        )

        size_parameters = map(int, stream.readline().split())

        number_of_states = next(size_parameters)
        number_of_input_symbols = next(size_parameters)
        number_of_tape_symbols = next(size_parameters)
        number_of_transitions = next(size_parameters)

        states = list(stream.readline().split())

        quintuple_machine_definition.initial_state = states[0]
        quintuple_machine_definition.final_states = list(states[-1])
        
        input_symbols = list(stream.readline().split())
        tape_symbols = list(stream.readline().split())

        quintuple_machine_definition.alphabet = tape_symbols

        for _ in range(number_of_transitions):
            quintuple_machine_definition.transitions.append(QuintupleTransition.parse(stream.readline()))
        
        return quintuple_machine_definition
