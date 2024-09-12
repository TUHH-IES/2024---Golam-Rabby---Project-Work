import random
import polars as pl
from typing import List, Union, Dict
from coffee import CoffeeMachine, StatusCode  



def generate_random_input() -> str:
    return random.choice(['water', 'pod', 'button', 'clean'])



def generate_random_data(steps: int) -> pl.DataFrame:
    coffee_machine: CoffeeMachine = CoffeeMachine()
    data: List[Dict[str, Union[int, str]]] = []

    for step in range(steps):
        input_alphabet: str = generate_random_input()
        output_alphabet_value: int = coffee_machine.transition(input_alphabet)  
        output_alphabet: StatusCode = StatusCode(output_alphabet_value)  
        current_state: str = coffee_machine.get_current_state()

        data.append({
            "step": step + 1,
            "input_alphabet": input_alphabet,
            "output_alphabet": output_alphabet.value,  
            "current_state": current_state
        })

    df: pl.DataFrame = pl.DataFrame(data)
    return df


def save_dataframe_to_csv(df: pl.DataFrame, filename: str) -> None:
    df.write_csv(filename)
    print(f"Data has been saved to {filename}")


if __name__ == "__main__":
    num_steps: int = random.randint(5, 10)
    random_data_df: pl.DataFrame = generate_random_data(num_steps)

    print(random_data_df)
    save_dataframe_to_csv(random_data_df, "coffee_machine_random_data.csv")
