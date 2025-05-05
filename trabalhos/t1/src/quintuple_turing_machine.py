from typing import Any, Self, List, TextIO
from dataclasses import dataclass
from collections import Counter
import re

from direction import Direction
from state import format_state_for_code
from mark import format_mark_for_code

@dataclass(order=True)
class QuintupleAct:
    read: Any
    write: Any
    direction: Direction

    def to_code(self) -> str:
        return (
            'QuintupleAct('
            f'{format_mark_for_code(self.read)}, '
            f'{format_mark_for_code(self.write)}, '
            f'{self.direction.to_code()}'
            ')'
        )

@dataclass(order=True)
class QuintupleTransition:
    source_state: int
    destination_state: int
    acts: List[QuintupleAct]

    def to_code(self) -> str:
        result = f'QuintupleTransition(\n'
        result += f"    source_state={format_state_for_code(self.source_state)},\n"
        result += f"    destination_state={format_state_for_code(self.destination_state)},\n"
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

    def to_code(self) -> str:
        result = f'QuintupleTuringMachineDefinition(\n'
        result += f"    tapes={self.tapes},\n"
        result += f"    alphabet=[{', '.join(map(format_mark_for_code, self.alphabet))}],\n"
        result += f"    transitions=[\n"

        for transition in self.transitions:
            lines = transition.to_code().splitlines()
            
            for line in lines[:-1]:
                result += f"        {line}\n"
            
            result += f"        {lines[-1]},\n"
        
        result += f"    ],\n"
        result += f"    initial_state={format_state_for_code(self.initial_state)},\n"
        result += f"    final_states=[{', '.join(map(format_state_for_code, self.final_states))}]\n"
        result += f")"

        return result
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, QuintupleTuringMachineDefinition):
            return False

        return (
            self.tapes == value.tapes and
            Counter(self.alphabet) == Counter(value.alphabet) and
            sorted(self.transitions) == sorted(value.transitions) and
            self.initial_state == value.initial_state and
            Counter(self.final_states) == Counter(value.final_states)
        )

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
