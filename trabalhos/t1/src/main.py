import sys

from quintuple_turing_machine import QuintupleTuringMachineDefinition
from quadruple_turing_machine import QuadrupleTuringMachineSimulator
from benett_reversibility import create_reversible_machine

from gui.gui import GUI

def read_quintuple_machine_definition() -> QuintupleTuringMachineDefinition:
    return QuintupleTuringMachineDefinition.parse(sys.stdin)

def read_quintuple_machine_initial_state():
    return list(input())

if __name__ == '__main__':
    quintuple_machine_definition = read_quintuple_machine_definition()
    quintuple_machine_initial_state = read_quintuple_machine_initial_state()

    quadruple_machine_definition = create_reversible_machine(quintuple_machine_definition)
    quadruple_machine_simulator = QuadrupleTuringMachineSimulator(quadruple_machine_definition)

    quadruple_machine_simulator.tapes[0].overwrite(quintuple_machine_initial_state, 1)

    gui = GUI(quadruple_machine_simulator, quadruple_machine_definition.transitions)

    gui.run()
 