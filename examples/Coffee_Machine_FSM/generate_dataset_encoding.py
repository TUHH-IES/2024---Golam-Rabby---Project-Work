import random
import polars as pl
from typing import List, Union, Dict
from coffee import CoffeeMachine, StatusCode


# categorical encoding for->input_alphabet 
input_alphabet_encoding = {
    'water': 0,
    'pod': 1,
    'button': 2,
    'clean': 3
}

# categorical encoding for->current_state
current_state_encoding = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'd_prime': 4,
    'e': 5,
    'f': 6
}


def generate_random_input() -> str:
    return random.choice(['water', 'pod', 'button', 'clean'])


def encode_alphabet(alphabet: str) -> int:
    return input_alphabet_encoding.get(alphabet, -1)  


def encode_current_state(state: str) -> int:
    return current_state_encoding.get(state, -1)  


def generate_random_data(steps: int) -> pl.DataFrame:
    coffee_machine: CoffeeMachine = CoffeeMachine()
    data: List[Dict[str, Union[int, str, float]]] = []

    for step in range(steps):
        # Generate random input
        input_alphabet: str = generate_random_input()
        
        
        output_alphabet_value: int = coffee_machine.transition(input_alphabet)
        output_alphabet: StatusCode = StatusCode(output_alphabet_value)
        current_state: str = coffee_machine.get_current_state()

        
        data.append({
            "step": step + 1,  
            "input_alphabet": encode_alphabet(input_alphabet),  
            "output_alphabet": output_alphabet.value,  
            "current_state": encode_current_state(current_state)  
        })

    # A Polars DataFrame creation from the generated data
    df: pl.DataFrame = pl.DataFrame(data)
    return df


def save_dataframe_to_csv(df: pl.DataFrame, filename: str) -> None:
    """Saving the Polars DataFrame to a CSV file."""
    df.write_csv(filename)
    print(f"Data has been saved to {filename}")


if __name__ == "__main__":
    num_steps: int = random.randint(5, 10)
    random_data_df: pl.DataFrame = generate_random_data(num_steps)

    # Displaying the generated DataFrame
    print(random_data_df)

    # Saving the generated data to a CSV file
    save_dataframe_to_csv(random_data_df, "coffee_machine_random_data.csv")
