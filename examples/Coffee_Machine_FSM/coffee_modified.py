
class CoffeeMachine:
    def __init__(self):
        self.state_a = StateA('a', self)  # Create an instance of StateA.
        self.state_b = StateB('b', self)  # Create an instance of StateB.
        self.state_c = StateC('c', self)  # Create an instance of StateC.
        self.state_d = StateD('d', self)  # Create an instance of StateD.
        self.state_d_prime = StateDPrime('d_prime', self)  # Create an instance of StateDPrime.
        self.state_e = StateE('e', self)  # Create an instance of StateE.
        self.state_f = StateF('f', self)  # Create an instance of StateF.

        self.current_state = self.state_a  # Setting the initial state of the coffee machine to state 'a'.

    def transition(self, input_alphabet):
        return self.current_state.transition(input_alphabet)  

    # Method to retrieve the current state's name.
    def get_current_state(self):
        return self.current_state.name  # Return the name of the current state.


# Base class representing a state in the coffee machine's finite state machine (FSM).
class State:
    def __init__(self, name, coffee_machine):
        self.name = name  # The name of the state, such as 'a', 'b', etc.
        self.coffee_machine = coffee_machine  

    # Abstract method to handle input.
    def handle_input(self, input_alphabet):
        raise NotImplementedError("This method would be implemented by subclasses")

    # Abstract method to handle output.
    def handle_output(self, input_alphabet):
        raise NotImplementedError("This method would be implemented by subclasses")

    # Abstract method for the transition to the next state. T
    def transition(self, input_alphabet):
        raise NotImplementedError("This method would be implemented by subclasses")



class StateA(State):
    def handle_input(self, input_alphabet):
        if input_alphabet == 'clean':
            return self.handle_output(input_alphabet)  # Stay in state 'a' if 'clean' is the input.
        elif input_alphabet == 'pod':
            return self.handle_output(input_alphabet)  # Stay in state 'a' if 'pod' is the input.
        elif input_alphabet == 'water':
            return self.handle_output(input_alphabet)  # Stay in state 'a' if 'water' is the input.
        elif input_alphabet == 'button':
            return self.handle_output(input_alphabet)  # Stay in state 'a' if 'button' is the input.
        return 0  # If the input is not recognized, return an error -> 0

    def handle_output(self, input_alphabet):
        if input_alphabet in ['clean', 'pod', 'water']:
            return 1  # returning integer value 1 instead of string-> 'OK'.
        elif input_alphabet == 'button':
            return 0  # returning integer value 0 instead of string-> 'error'.
        return 0  # Default to integer value-> 0 (error) if the input alphabet doesn't match the expected inputs.

    def transition(self, input_alphabet):
        output_alphabet = self.handle_input(input_alphabet)  
        if input_alphabet == 'clean':
            self.coffee_machine.current_state = self  
        elif input_alphabet == 'pod':
            self.coffee_machine.current_state = self.coffee_machine.state_b  # Transition to state 'b'.
        elif input_alphabet == 'water':
            self.coffee_machine.current_state = self.coffee_machine.state_c  # Transition to state 'c'.
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_f  # Transition to state 'f'.
        return output_alphabet  # Return the output after handling the transition.


# StateB class 
class StateB(State):
    def handle_input(self, input_alphabet):
        if input_alphabet == 'clean':
            return self.handle_output(input_alphabet)  # Transition to 'a' if clean is pressed.
        elif input_alphabet == 'pod':
            return self.handle_output(input_alphabet)  # Stay in 'b'.
        elif input_alphabet == 'water':
            return self.handle_output(input_alphabet)  # Transition to 'd'.
        elif input_alphabet == 'button':
            return self.handle_output(input_alphabet)  # Transition to 'f'.
        return 0  # If the input is not recognized, return an error -> 0

    def handle_output(self, input_alphabet):
        if input_alphabet in ['clean', 'pod', 'water']:
            return 1  
        elif input_alphabet == 'button':
            return 0  
        return 0  # If the input is not recognized, return an error -> 0

    def transition(self, input_alphabet):
        output_alphabet = self.handle_input(input_alphabet) 
        if input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a  # Transition to 'a'.
        elif input_alphabet == 'pod':
            self.coffee_machine.current_state = self  # Stay in 'b'.
        elif input_alphabet == 'water':
            self.coffee_machine.current_state = self.coffee_machine.state_d  # Transition to 'd'.
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_f  # Transition to 'f'.
        return output_alphabet  

# StateC class 
class StateC(State):
    def handle_input(self, input_alphabet):
        if input_alphabet == 'clean':
            return self.handle_output(input_alphabet)  # Transition to 'a' if clean is pressed.
        elif input_alphabet == 'water':
            return self.handle_output(input_alphabet)  # Stay in 'c'.
        elif input_alphabet == 'pod':
            return self.handle_output(input_alphabet)  # Transition to 'd_prime'.
        elif input_alphabet == 'button':
            return self.handle_output(input_alphabet)  # Transition to 'f'.
        return 0 
    
    def handle_output(self, input_alphabet):
        if input_alphabet in ['clean', 'pod', 'water']:
            return 1  
        elif input_alphabet == 'button':
            return 0  
        return 0  

    def transition(self, input_alphabet):
        output_alphabet = self.handle_input(input_alphabet)  
        if input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a  # Transition to 'a'.
        elif input_alphabet == 'water':
            self.coffee_machine.current_state = self  # Stay in 'c'.
        elif input_alphabet == 'pod':
            self.coffee_machine.current_state = self.coffee_machine.state_d_prime  # Transition to 'd_prime'.
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_f  # Transition to 'f'.
        return output_alphabet  

# StateD class
class StateD(State):
    def handle_input(self, input_alphabet):
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            return self.handle_output(input_alphabet)  # Stay in 'd'.
        elif input_alphabet == 'button':
            return self.handle_output(input_alphabet)  # Transition to 'e'.
        elif input_alphabet == 'clean':
            return self.handle_output(input_alphabet)  # Transition to 'a'.
        return 0  # Default error case.

    def handle_output(self, input_alphabet):
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            return 1  
        elif input_alphabet == 'button':
            return 2  
        return 0  
    
    def transition(self, input_alphabet):
        output_alphabet = self.handle_input(input_alphabet)  
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            self.coffee_machine.current_state = self  # Stay in 'd'.
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_e  # Transition to 'e'.
        elif input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a  # Transition to 'a'.
        return output_alphabet 
    

# StateDPrime class
class StateDPrime(State):
    def handle_input(self, input_alphabet):
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            return self.handle_output(input_alphabet)  # Stay in 'd_prime'.
        elif input_alphabet == 'button':
            return self.handle_output(input_alphabet)  # Transition to 'e'.
        elif input_alphabet == 'clean':
            return self.handle_output(input_alphabet)  # Transition to 'a'.
        return 0  

    def handle_output(self, input_alphabet):
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            return 1 
        elif input_alphabet == 'button':
            return 2 
        return 0  

    def transition(self, input_alphabet):
        output_alphabet = self.handle_input(input_alphabet)  #
        if isinstance(input_alphabet, list) and all(item in ['water', 'pod'] for item in input_alphabet):
            self.coffee_machine.current_state = self  # Stay in 'd_prime'.
        elif input_alphabet == 'button':
            self.coffee_machine.current_state = self.coffee_machine.state_e  # Transition to 'e'.
        elif input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a  # Transition to 'a'.
        return output_alphabet  


# StateE class
class StateE(State):
    def handle_input(self, input_alphabet):
        if input_alphabet == 'clean':
            return self.handle_output(input_alphabet)  # Transition to 'a'.
        return 0 

    def handle_output(self, input_alphabet):
        if input_alphabet == 'clean':
            return 1 
        return 0  

    def transition(self, input_alphabet):
        output_alphabet = self.handle_input(input_alphabet)  
        if input_alphabet == 'clean':
            self.coffee_machine.current_state = self.coffee_machine.state_a  # Transition to 'a'.
        else:
            self.coffee_machine.current_state = self.coffee_machine.state_f  # Transition to 'f'.
        return output_alphabet  


# StateF class 
class StateF(State):
    def handle_input(self, input_alphabet):
        return self.handle_output(input_alphabet)  # Always produce 'error' (0) output.

    def handle_output(self, input_alphabet):
        return 0  

    def transition(self, input_alphabet):
        return self.handle_input(input_alphabet)  


#  Simulation function for the coffee machine to test the behaviour of the FSM.
def interactive_coffee_machine():
    coffee_machine = CoffeeMachine()  

    print("Welcome to the Coffee Machine Test Simulation!")
    
    while True:
        current_state = coffee_machine.get_current_state()  # Get the current state.
        print(f"\nCurrent state: {current_state}")

        user_input = input("Enter an input alphabet (water, pod, button, clean) or multiple input alphabets separated by a comma (e.g., 'water,pod'), or 'exit' to stop: ").lower()

        if user_input == 'exit':  
            print("Exiting the coffee machine simulator!!")
            break
        
      
        inputs = [i.strip() for i in user_input.split(',')]
        
        # Validating the inputs to ensure they're allowed options.
        if any(i not in ['water', 'pod', 'button', 'clean'] for i in inputs):
            print("Invalid input. Please enter 'water', 'pod', 'button', or 'clean'.")
            continue

        if len(inputs) == 1:
            inputs = inputs[0]

        
        output_alphabet = coffee_machine.transition(inputs)
        
        # Display the result after the state transition.
        new_state = coffee_machine.get_current_state()
        print(f"Input: {user_input} -> Output: {output_alphabet}, New State: {new_state}")



# Entry point of the program.
if __name__ == '__main__':
    interactive_coffee_machine()
