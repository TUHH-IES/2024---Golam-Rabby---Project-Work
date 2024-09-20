# flowcean_Linear_Regression.py

import logging
import random
import polars as pl

import flowcean.cli
from flowcean.environments.dataset import Dataset  
from flowcean.environments.train_test_split import TrainTestSplit
from flowcean.learners.linear_regression import LinearRegression
from flowcean.metrics import MeanAbsoluteError, MeanSquaredError
from flowcean.strategies.incremental import learn_incremental
from flowcean.strategies.offline import evaluate_offline


from generate_dataset_float import generate_random_data


logger = logging.getLogger(__name__)


def main() -> None:
    flowcean.cli.initialize_logging()
    logger.info("Flowcean logging has been initialized.")

    num_steps: int = random.randint(5, 50)
    logger.info(f"Generating random datasets with {num_steps} steps.")

    df: pl.DataFrame = generate_random_data(num_steps)

    try:
        data: Dataset = Dataset(df)
        logger.info("Dataset instantiated with Flowcean's Dataset class.")
    except TypeError as e:
        logger.error(f"Failed to instantiate Flowcean's Dataset: {e}")
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

    # Initializing the Linear Regression learner
    try:
        learner = LinearRegression(
            input_size=1,
            output_size=1,
            learning_rate=0.01,
        )
        logger.info("Linear Regression learner has been initialized.")
    except Exception as e:
        logger.error(f"Error initializing Linear Regression learner: {e}")
        return  
    inputs = ["input_sequence"]  
    outputs = ["output_sequence"]

    try:
        model = learn_incremental(
            train.as_stream(batch_size=10).load(),
            learner,
            inputs,
            outputs,
        )
        logger.info("Model has been trained incrementally using the training data stream.")
    except Exception as e:
        logger.error(f"Error during incremental learning: {e}")
        return

    metrics = [MeanAbsoluteError(), MeanSquaredError()]
    logger.info("Evaluation metrics defined: Mean Absolute Error, Mean Squared Error.")

    try:
        report = evaluate_offline(
            model,
            test,
            inputs,
            outputs,
            metrics,
        )
        logger.info("Model evaluation on test set has been completed.")
    except Exception as e:
        logger.error(f"Error during model evaluation: {e}")
        return

    print("Model Evaluation Report:")
    print(report)


if __name__ == "__main__":
    main()
