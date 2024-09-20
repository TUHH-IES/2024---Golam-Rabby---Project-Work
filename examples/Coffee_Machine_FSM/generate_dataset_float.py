#dataset_generation.py

import random
import polars as pl
from typing import List, Union, Dict
from coffee_abstract import CoffeeMachine

# Categorical encoding for input_sequence
input_sequence_encoding = {
    'water': 0,
    'pod': 1,
    'button': 2,
    'clean': 3
}

# Categorical encoding for current_state
current_state_encoding = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'd_prime': 4,
    'e': 5,
    'f': 6
}

def generate_random_input() -> Union[str, List[str]]:
    possible_inputs = [
        'water',
        'pod',
        'button',
        'clean'
    ]
    return random.choice(possible_inputs)

def encode_input_sequence(input_sequence: Union[str, List[str]]) -> int:
    
    return input_sequence_encoding.get(input_sequence, -1)

def encode_current_state(state: str) -> int:

    return current_state_encoding.get(state, -1)


def generate_random_data(steps: int) -> pl.DataFrame:

    coffee_machine: CoffeeMachine = CoffeeMachine()
    data: List[Dict[str, Union[float, int]]] = []

    for step in range(steps):
        # Generating random input_sequence
        input_sequence: Union[str, List[str]] = generate_random_input()

        # Processing the input through the coffee machine
        output_sequence: int = coffee_machine.transition(input_sequence)
        current_state: str = coffee_machine.get_current_state()

        encoded_input_sequence: int = encode_input_sequence(input_sequence)
        encoded_current_state: int = encode_current_state(current_state)

        data.append({
            "step": float(step + 1),  
            "input_sequence": float(encoded_input_sequence),  
            "output_sequence": float(output_sequence),        
            "current_state": float(encoded_current_state)     
        })

    # Creating a Polars DataFrame from the data
    df: pl.DataFrame = pl.DataFrame(data)
    
    # Casting relevant columns to Float32-type
    df = df.with_columns([
        pl.col("input_sequence").cast(pl.Float32),
        pl.col("output_sequence").cast(pl.Float32),
        pl.col("current_state").cast(pl.Float32)
    ])
    
    return df

def save_dataframe_to_csv(df: pl.DataFrame, filename: str) -> None:

    df.write_csv(filename)
    print(f"Data has been saved to {filename}")

if __name__ == "__main__":
    num_steps: int = random.randint(5, 10)
    random_data_df: pl.DataFrame = generate_random_data(num_steps)

    # Displaying the generated DataFrame
    print(random_data_df)

    # Saving the generated data to a CSV file
    save_dataframe_to_csv(random_data_df, "coffee_machine_random_data.csv")
