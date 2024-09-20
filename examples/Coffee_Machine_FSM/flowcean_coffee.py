import logging

import flowcean.cli
from flowcean.environments.uri import UriDataLoader
from flowcean.environments.train_test_split import TrainTestSplit
from flowcean.learners.lightning import LightningLearner, MultilayerPerceptron
from flowcean.metrics import MeanAbsoluteError, MeanSquaredError
from flowcean.strategies.offline import learn_offline, evaluate_offline
from flowcean.transforms import Select, Standardize

logger = logging.getLogger(__name__)

def main() -> None:
    # Initialization of logging
    flowcean.cli.initialize_logging()

    data = UriDataLoader(uri="file:./coffee_machine_random_data.csv").with_transform(
        Select(["step", "input_alphabet", "output_alphabet", "current_state"])
    )
    data.load()

    # Splitting the data into training and testing sets (80% train, 20% test)
    train, test = TrainTestSplit(ratio=0.8, shuffle=True).split(data)


    transform = Standardize()
    
    learner = LightningLearner(
        module=MultilayerPerceptron(
            learning_rate=1e-3,
            input_size=3,  
            output_size=1,  
            hidden_dimensions=[10, 10],  
        ),
        max_epochs=20,
    )

    # inputs and outputs feature specification
    inputs = ["step", "input_alphabet", "output_alphabet"]
    outputs = ["current_state"]

    # Training the model using the training data
    model = learn_offline(
        train,
        learner,
        inputs,
        outputs,
        input_transform=transform,
    )

    # Evaluating the model
    report = evaluate_offline(
        model,
        test,
        inputs,
        outputs,
        [MeanAbsoluteError(), MeanSquaredError()],
    )

    # Evaluation of results
    print(report)

if __name__ == "__main__":
    main()
