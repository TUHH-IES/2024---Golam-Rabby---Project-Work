from abc import ABC, abstractmethod
from enum import Enum
from typing import Union, List, Tuple


class StatusCode(Enum):
    OK = 1
    ERROR = 0
    COFFEE_PRODUCED = 2


class State(ABC):
    """
    Abstract base class for representing a state in the coffee machine FSM.
    """
    name: str  # Class variable for the state's name

    @abstractmethod
    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        """
        Processes the input sequence and returns a tuple of (output sequence, next state).
        """
        pass
"""
Feedback covered->
    01->> ""I wouldn't call it alphabet, because the alphabet usually means all possible inputs, 
            but here it is an example input. I would rather call it input_sequence or just inputs, here.""

    02->> ""This function seems to be unnecessary because it just calls another function.""
"""

class CoffeeMachine:
    def __init__(self) -> None:
        self.current_state: State = StateA()  # Initial state

    def transition(self, input_sequence: Union[str, List[str]]) -> int:
        output_sequence, next_state = self.current_state.process(input_sequence)
        self.current_state = next_state
        return output_sequence

    def get_current_state(self) -> str:
        return self.current_state.name


class StateA(State):
    name = 'a'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        if input_sequence == 'clean':
            return StatusCode.OK.value, self  # Stay in state->'a'
        elif input_sequence == 'pod':
            return StatusCode.OK.value, StateB()
        elif input_sequence == 'water':
            return StatusCode.OK.value, StateC()
        elif input_sequence == 'button':
            return StatusCode.ERROR.value, StateF()
        else:
            return StatusCode.ERROR.value, StateF()
        


class StateB(State):
    name = 'b'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        if input_sequence == 'clean':
            return StatusCode.OK.value, StateA()
        elif input_sequence == 'pod':
            return StatusCode.OK.value, self  # Stay in state->'b'
        elif input_sequence == 'water':
            return StatusCode.OK.value, StateD()
        elif input_sequence == 'button':
            return StatusCode.ERROR.value, StateF()
        else:
            return StatusCode.ERROR.value, StateF()
        


class StateC(State):
    name = 'c'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        if input_sequence == 'clean':
            return StatusCode.OK.value, StateA()
        elif input_sequence == 'water':
            return StatusCode.OK.value, self  # Stay in state->'c'
        elif input_sequence == 'pod':
            return StatusCode.OK.value, StateDPrime()
        elif input_sequence == 'button':
            return StatusCode.ERROR.value, StateF()
        else:
            return StatusCode.ERROR.value, StateF()
        


class StateD(State):
    name = 'd'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        if input_sequence in ['water', 'pod']:
            return StatusCode.OK.value, self  # Stay in state->'d'
        elif input_sequence == 'button':
            return StatusCode.COFFEE_PRODUCED.value, StateE()
        elif input_sequence == 'clean':
            return StatusCode.OK.value, StateA()
        else:
            return StatusCode.ERROR.value, StateF()
        


class StateDPrime(State):
    name = 'd_prime'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        if input_sequence in ['water', 'pod']:
            return StatusCode.OK.value, self  # Stay in state->'d_prime'
        elif input_sequence == 'button':
            return StatusCode.COFFEE_PRODUCED.value, StateE()
        elif input_sequence == 'clean':
            return StatusCode.OK.value, StateA()
        else:
            return StatusCode.ERROR.value, StateF()
        


class StateE(State):
    name = 'e'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        if input_sequence == 'clean':
            return StatusCode.OK.value, StateA()
        else:
            return StatusCode.ERROR.value, StateF()


class StateF(State):
    name = 'f'

    def process(self, input_sequence: Union[str, List[str]]) -> Tuple[int, 'State']:
        return StatusCode.ERROR.value, self  # Stay in state->'f'
