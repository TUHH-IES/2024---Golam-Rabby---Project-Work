# flowcean_regression_tree.py

import logging
import random
import polars as pl
from generate_dataset_float import generate_random_data

import flowcean.cli
from flowcean.environments.dataset import Dataset
from flowcean.environments.train_test_split import TrainTestSplit
from flowcean.learners.regression_tree import RegressionTree
from flowcean.metrics.regression import MeanAbsoluteError, MeanSquaredError
from flowcean.strategies.offline import evaluate_offline, learn_offline



logger = logging.getLogger(__name__)

def main() -> None:
    flowcean.cli.initialize_logging()
    logger.info("Flowcean logging has been initialized.")

    num_steps: int = random.randint(5, 40)
    logger.info(f"Generating random dataset with {num_steps} steps.")
    df: pl.DataFrame = generate_random_data(num_steps)

    try:
        data: Dataset = Dataset(df)
        logger.info("Dataset instantiated with Flowcean's Dataset class.")
    except TypeError as e:
        logger.error(f"Failed to instantiate-> Flowcean's Dataset: {e}")
        return

    try:
        data.load()
        logger.info("Dataset has been loaded into Flowcean's environment.")
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return

    try:
        train, test = TrainTestSplit(ratio=0.8, shuffle=False).split(data)
        logger.info("Dataset split into training and testing sets.")
    except Exception as e:
        logger.error(f"Error during train-test split: {e}")
        return

    # Initializing Regression Tree Learner
    learner = RegressionTree()
    inputs = ["input_sequence"] 
    outputs = ["output_sequence"]
    model = learn_offline(
        train,
        learner,
        inputs,
        outputs,
    )
    logger.info("Model has been trained successfully")   
    report = evaluate_offline(
        model,
        test,
        inputs,
        outputs,
        [MeanAbsoluteError(), MeanSquaredError()],
    )
    logger.info("Model evaluation has been completed")
    print(report)

if __name__ == "__main__":
    main()
