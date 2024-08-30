import random
import polars as pl
from coffee_modified import CoffeeMachine  # Importing the CoffeeMachine class from coffee_modified.py

# Function to generate a random dataset for the Coffee Machine FSM
def generate_random_dataset(coffee_machine, num_steps):
    input_alphabets = ['water', 'pod', 'button', 'clean']  # Defining the inputs-> input alphabet
    dataset = []  
    
    for _ in range(num_steps):
        current_state = coffee_machine.get_current_state()  
        
        if current_state == 'f':
            input_alphabet = input_alphabets  # All inputs are given in state 'f'
        elif current_state in ['d', 'd_prime'] and random.choice([True, False]):
            input_alphabet = ['water', 'pod']  # Combination of 'water' and 'pod' inputs
        else:
            input_alphabet = random.choice(input_alphabets)  # Single random input
        
        output_alphabet = coffee_machine.transition(input_alphabet) 
        current_state = coffee_machine.get_current_state()  
        
        # Append the input, output, and state to the dataset
        dataset.append({
            'Input Alphabet': input_alphabet if isinstance(input_alphabet, str) else ','.join(input_alphabet),
            'Output Alphabet': output_alphabet,
            'Current State': current_state
        })
    
    return dataset

# Function to generate a random dataset with a random number of steps
def generate_random_coffee_machine_dataset():
    coffee_machine = CoffeeMachine()  
    num_steps = random.randint(5, 20)  
    
    dataset = generate_random_dataset(coffee_machine, num_steps)  # Generating the dataset
    
    # Converting the dataset to a Polars DataFrame
    df = pl.DataFrame(dataset)
    
    # Save the dataset as a CSV file
    df.write_csv("coffee_machine_dataset.csv")
    
    return df

# Main function to generate and print the dataset
if __name__ == '__main__':
    random_dataset = generate_random_coffee_machine_dataset()
    print(random_dataset)
