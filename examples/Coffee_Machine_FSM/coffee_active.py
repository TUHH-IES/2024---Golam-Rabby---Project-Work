# active_learning.py

import logging
from pathlib import Path
from typing import Optional, List, Dict
import polars as pl
from dataclasses import dataclass

from coffee_abstract import CoffeeMachine, StatusCode, StateA  
import flowcean.cli
from flowcean.core import ActiveEnvironment, ActiveLearner, Model
from flowcean.strategies.active import learn_active, StopLearning

# logger Configuration
logger = logging.getLogger(__name__)

# Definition of Action and Observation Types
Action = str  # Possible actions from coffee_fsm: 'pod', 'water', 'button', 'clean'

@dataclass
class CoffeeObservation:
    status_code: StatusCode
    previous_state: str
    current_state: str

# ============================
# CoffeeEnvironment Class
# ============================
class CoffeeEnvironment(ActiveEnvironment[Action, CoffeeObservation]):
    def __init__(self, max_num_iterations: int):
        self.coffee_machine = CoffeeMachine()
        self.last_action: Optional[Action] = None
        self.status_code = StatusCode.OK
        self.max_num_iterations = max_num_iterations
        self.current_iteration = 0
        self.previous_state = self.coffee_machine.get_current_state()

    def load(self) -> 'CoffeeEnvironment':
        return self

    def act(self, action: Action) -> None:
        self.last_action = action

    def step(self) -> None:
        if self.last_action is None:
            raise ValueError("No action taken yet")
        # Record the state before the action
        self.previous_state = self.coffee_machine.get_current_state()
        output_sequence = self.coffee_machine.transition(self.last_action)
        self.status_code = StatusCode(output_sequence)
        logger.debug(f"Action: {self.last_action}, Previous State: {self.previous_state}, Status: {self.status_code}")
        self.current_iteration += 1
        if self.current_iteration >= self.max_num_iterations:
            raise StopLearning()
        if self.status_code == StatusCode.ERROR or self.status_code == StatusCode.COFFEE_PRODUCED:
            # Reseting the coffee machine to initial state after error or coffee produced
            self.coffee_machine.current_state = StateA()

    def observe(self) -> CoffeeObservation:
        return CoffeeObservation(
            status_code=self.status_code,
            previous_state=self.previous_state,
            current_state=self.coffee_machine.get_current_state(),
        )

# ============================
# CoffeeModel Class
# ============================
class CoffeeModel(Model):
    def __init__(self):
        # Storing the best action per state
        self.best_actions: Dict[str, Action] = {}

    def predict(self, input_features: pl.DataFrame) -> pl.DataFrame:
        actions = []
        for state in input_features['current_state']:
            if state in self.best_actions:
                actions.append(self.best_actions[state])
            else:
                # Default action if state is unknown
                actions.append('clean')
        return pl.DataFrame({'action': actions})

    def save(self, path: Path) -> None:
        pass

    def load(self, path: Path) -> None:
        pass

# ============================
# CoffeeLearner Class
# ============================
class CoffeeLearner(ActiveLearner[Action, CoffeeObservation]):
    def __init__(self):
        self.model = CoffeeModel()
        self.rewards: List[float] = []
        self.actions = ['water', 'pod', 'button', 'clean']
        self.state_action_rewards: Dict[str, Dict[str, float]] = {}
        self.action_indices: Dict[str, int] = {}

    def learn_active(self, action: Action, observation: CoffeeObservation) -> Model:
        status_code = observation.status_code
        previous_state = observation.previous_state

        # Assigning rewards based on status_code
        if status_code == StatusCode.COFFEE_PRODUCED:
            reward = 1.0
            self.model.best_actions[previous_state] = action
        elif status_code == StatusCode.OK:
            reward = 0.5
        elif status_code == StatusCode.ERROR:
            reward = -1.0
        else:
            reward = 0.0  

        self.rewards.append(reward)

        # Updating state-action rewards
        if previous_state not in self.state_action_rewards:
            self.state_action_rewards[previous_state] = {action: reward}
        else:
            self.state_action_rewards[previous_state][action] = reward

        logger.debug(f"Learned: State: {previous_state}, Action: {action}, Reward: {reward}")

        return self.model

    def propose_action(self, observation: CoffeeObservation) -> Action:
        current_state = observation.current_state

        if current_state == 'f':
            return 'clean'  

        if current_state in self.model.best_actions:
            return self.model.best_actions[current_state]
        else:
            if current_state not in self.action_indices:
                self.action_indices[current_state] = 0

            index = self.action_indices[current_state]
            while index < len(self.actions):
                action = self.actions[index]
                if action in self.state_action_rewards.get(current_state, {}) and self.state_action_rewards[current_state][action] == -1.0:
                    index += 1
                else:
                    self.action_indices[current_state] = index + 1
                    return action
            return 'clean'

# ============================
# Main Function
# ============================
def main() -> None:
    flowcean.cli.initialize_logging()
    logger.setLevel(logging.DEBUG)
    logger.info("Initiation of Active Learning with Coffee Machine Environment")

    max_iterations = 50
    environment = CoffeeEnvironment(max_num_iterations=max_iterations)

    learner = CoffeeLearner()

    try:
        model = learn_active(environment, learner)
    except StopLearning:
        logger.info("Learning process stopped by StopLearning exception.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during learning: {e}")
    finally:
        logger.info("Active Learning process completed.")

    if learner.model.best_actions:
        print("\nBest Action per State Learned:")
        for state, action in learner.model.best_actions.items():
            print(f"State '{state}': {action}")
    else:
        print("No valid action was learned.")

    print(f"\nTotal Rewards Collected: {len(learner.rewards)}")
    if learner.rewards:
        print(f"Rewards: {learner.rewards}")

if __name__ == "__main__":
    main()
