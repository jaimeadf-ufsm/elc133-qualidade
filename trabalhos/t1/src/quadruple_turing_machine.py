from typing import Any, Optional, List
from dataclasses import dataclass
from enum import Enum, auto

from direction import Direction
from tape import Tape
from mark import format_mark_for_display, format_mark_for_code

class QuadrupleActType(Enum):
    SHIFT = auto()
    READ_WRITE = auto()

@dataclass
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

@dataclass
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
        result += f"    source_state='{self.source_state}',\n"
        result += f"    destination_state='{self.destination_state}',\n"
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
        