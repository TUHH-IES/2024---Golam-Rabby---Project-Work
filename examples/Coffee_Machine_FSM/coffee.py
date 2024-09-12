from enum import Enum
from typing import Union, List



class StatusCode(Enum):
    OK = 1
    ERROR = 0
    COFFEE_PRODUCED = 2



class State:
    def __init__(self, name: str, coffee_machine: "CoffeeMachine") -> None:
        self.name: str = name
        self.coffee_machine: CoffeeMachine = coffee_machine

    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        raise NotImplementedError("This method will be implemented by subclasses")

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        raise NotImplementedError("This method will be implemented by subclasses")

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        raise NotImplementedError("This method will be implemented by subclasses")



class CoffeeMachine:
    def __init__(self) -> None:
        self.state_a = StateA('a', self)  
        self.state_b = StateB('b', self)  
        self.state_c = StateC('c', self)  
        self.state_d = StateD('d', self)  
        self.state_d_prime = StateDPrime('d_prime', self) 
        self.state_e = StateE('e', self)  
        self.state_f = StateF('f', self)  

        self.current_state: State = self.state_a  # Initial state of the coffee machine

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        try:
            return self.current_state.transition(input_alphabet)
        except Exception as e:
            print(f"Transition error: {e}")
            return StatusCode.ERROR.value  

    def get_current_state(self) -> str:
        return self.current_state.name  



class StateA(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        if isinstance(input_alphabet, str):
            if input_alphabet in ['clean', 'pod', 'water']:
                return StatusCode.OK.value
            elif input_alphabet == 'button':
                return StatusCode.ERROR.value
        return StatusCode.ERROR.value

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        output_alphabet: int = self.handle_input(input_alphabet)
        if isinstance(input_alphabet, str):
            if input_alphabet == 'clean':
                self.coffee_machine.current_state = self
            elif input_alphabet == 'pod':
                self.coffee_machine.current_state = self.coffee_machine.state_b
            elif input_alphabet == 'water':
                self.coffee_machine.current_state = self.coffee_machine.state_c
            elif input_alphabet == 'button':
                self.coffee_machine.current_state = self.coffee_machine.state_f
        return output_alphabet


class StateB(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        if isinstance(input_alphabet, str):
            if input_alphabet in ['clean', 'pod', 'water']:
                return StatusCode.OK.value
            elif input_alphabet == 'button':
                return StatusCode.ERROR.value
        return StatusCode.ERROR.value

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        output_alphabet: int = self.handle_input(input_alphabet)
        if isinstance(input_alphabet, str):
            if input_alphabet == 'clean':
                self.coffee_machine.current_state = self.coffee_machine.state_a
            elif input_alphabet == 'pod':
                self.coffee_machine.current_state = self
            elif input_alphabet == 'water':
                self.coffee_machine.current_state = self.coffee_machine.state_d
            elif input_alphabet == 'button':
                self.coffee_machine.current_state = self.coffee_machine.state_f
        return output_alphabet


class StateC(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        if isinstance(input_alphabet, str):
            if input_alphabet in ['clean', 'pod', 'water']:
                return StatusCode.OK.value
            elif input_alphabet == 'button':
                return StatusCode.ERROR.value
        return StatusCode.ERROR.value

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        output_alphabet: int = self.handle_input(input_alphabet)
        if isinstance(input_alphabet, str):
            if input_alphabet == 'clean':
                self.coffee_machine.current_state = self.coffee_machine.state_a
            elif input_alphabet == 'water':
                self.coffee_machine.current_state = self
            elif input_alphabet == 'pod':
                self.coffee_machine.current_state = self.coffee_machine.state_d_prime
            elif input_alphabet == 'button':
                self.coffee_machine.current_state = self.coffee_machine.state_f
        return output_alphabet


class StateD(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            return StatusCode.OK.value
        elif input_alphabet == 'button':
            return StatusCode.COFFEE_PRODUCED.value
        return StatusCode.ERROR.value

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        output_alphabet: int = self.handle_input(input_alphabet)
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            self.coffee_machine.current_state = self  
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_e
        elif input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a
        return output_alphabet


class StateDPrime(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            return StatusCode.OK.value
        elif input_alphabet == 'button':
            return StatusCode.COFFEE_PRODUCED.value
        return StatusCode.ERROR.value

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        output_alphabet: int = self.handle_input(input_alphabet)
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            self.coffee_machine.current_state = self  
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_e
        elif input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a
        return output_alphabet


class StateE(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        if input_alphabet == 'clean':
            return StatusCode.OK.value
        return StatusCode.ERROR.value

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        output_alphabet: int = self.handle_input(input_alphabet)
        if input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a
        else:
            self.coffee_machine.current_state = self.coffee_machine.state_f
        return output_alphabet


class StateF(State):
    def handle_input(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_output(input_alphabet)

    def handle_output(self, input_alphabet: Union[str, List[str]]) -> int:
        return StatusCode.ERROR.value  

    def transition(self, input_alphabet: Union[str, List[str]]) -> int:
        return self.handle_input(input_alphabet)
