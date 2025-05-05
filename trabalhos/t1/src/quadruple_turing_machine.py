from typing import Any, Optional, List
from dataclasses import dataclass
from collections import Counter
from enum import Enum, auto

from direction import Direction
from tape import Tape
from state import format_state_for_code
from mark import format_mark_for_display, format_mark_for_code

class QuadrupleActType(Enum):
    SHIFT = auto()
    READ_WRITE = auto()

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, QuadrupleActType):
            return False

        return self.value < other.value

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, QuadrupleActType):
            return False

        return self.value > other.value

@dataclass(order=True)
class QuadrupleAct:
    kind: QuadrupleActType
    direction: Optional[Direction] = None
    read: Optional[Any] = None
    write: Optional[Any] = None
    
    def to_code(self) -> str:
        if self.kind == QuadrupleActType.SHIFT:
            return f'QuadrupleAct.shift({self.direction.to_code()})'
        elif self.kind == QuadrupleActType.READ_WRITE:
            return f'QuadrupleAct.read_write(' \
                f'{format_mark_for_code(self.read)}, ' \
                f'{format_mark_for_code(self.write)})'
        else:
            raise ValueError(f'Unknown act type: {self.kind}')

    def shift(direction: Direction):
        return QuadrupleAct(
            kind=QuadrupleActType.SHIFT,
            direction=direction
        )
    
    def read_write(read: Any, write: Any):
        return QuadrupleAct(
            kind=QuadrupleActType.READ_WRITE,
            read=read,
            write=write
        )

@dataclass(order=True)
class QuadrupleTransition:
    source_state: str
    destination_state: str
    acts: List[QuadrupleAct]

    def matches(self, state: str, data: List[Any]) -> bool:
        if self.source_state != state:
            return False

        for i, act in enumerate(self.acts):
            if act.kind == QuadrupleActType.READ_WRITE and act.read != data[i]:
                return False

        return True
    
    def to_code(self):
        result = f'QuadrupleTransition(\n'
        result += f"    source_state={format_state_for_code(self.source_state)},\n"
        result += f"    destination_state={format_state_for_code(self.destination_state)},\n"
        result += f'    acts=[\n'
        
        for act in self.acts:
            result += f'        {act.to_code()},\n'

        result += f'    ]\n'
        result += f')'

        return result
    
    def __str__(self):
        inputs = []
        outputs = []
        
        for act in self.acts:
            if act.kind == QuadrupleActType.SHIFT:
                inputs.append('/')
                outputs.append(str(act.direction))
            elif act.kind == QuadrupleActType.READ_WRITE:
                inputs.append(format_mark_for_display(act.read))
                outputs.append(format_mark_for_display(act.write))
        
        result = self.source_state
        result += f'[{' '.join(inputs)}]'
        result += ' -> '
        result += f'[{' '.join(outputs)}]'
        result += self.destination_state

        return result

@dataclass
class QuadrupleTuringMachineDefinition:
    tapes: int
    alphabet: List[Any]
    transitions: List[QuadrupleTransition]
    initial_state: str
    final_states: List[str]

    def find_matching_transition(self, state: str, data: List[Any]) -> Optional[QuadrupleTransition]:
        for transition in self.transitions:
            if transition.matches(state, data):
                return transition

        return None
    
    def to_code(self) -> str:
        result = f'QuadrupleTuringMachineDefinition(\n'
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
        if not isinstance(value, QuadrupleTuringMachineDefinition):
            return False

        return (
            self.tapes == value.tapes and
            Counter(self.alphabet) == Counter(value.alphabet) and
            sorted(self.transitions) == sorted(value.transitions) and
            self.initial_state == value.initial_state and
            Counter(self.final_states) == Counter(value.final_states)
        )

class QuadrupleTuringMachineSimulator:
    definition: QuadrupleTuringMachineDefinition

    tapes: List[Tape]
    current_state: str

    def __init__(self, definition: QuadrupleTuringMachineDefinition):
        self.tapes = [Tape() for _ in range(definition.tapes)]

        self.definition = definition
        self.current_state = definition.initial_state
    
    def step(self):
        transition = self._find_next_transition()

        if transition is None:
            return None

        for i, act in enumerate(transition.acts):
            if act.kind == QuadrupleActType.READ_WRITE:
                self.tapes[i].write(act.write)
            elif act.kind == QuadrupleActType.SHIFT:
                self.tapes[i].shift(act.direction)
        
        self.current_state = transition.destination_state

        return transition
    
    def has_accepted(self) -> bool:
        return self.current_state in self.definition.final_states
    
    def has_rejected(self) -> bool:
        if self.has_accepted():
            return False

        return self.has_halted()
    
    def has_halted(self) -> bool:
        return self._find_next_transition() is None
    
    def _find_next_transition(self) -> Optional[QuadrupleTransition]:
        data = [tape.read() for tape in self.tapes]
        return self.definition.find_matching_transition(self.current_state, data)
        