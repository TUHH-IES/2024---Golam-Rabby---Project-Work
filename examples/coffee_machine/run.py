import flowcean.cli
from flowcean.environments.train_test_split import TrainTestSplit
from flowcean.environments.uri import UriDataLoader
from flowcean.learners.grpc.learner import GrpcLearner
from flowcean.metrics import MeanAbsoluteError, MeanSquaredError
from flowcean.strategies.offline import evaluate_offline, learn_offline


def main() -> None:
    flowcean.cli.initialize_logging()

    data = UriDataLoader(uri="file:./data/coffee_data.csv")
    data.load()
    train, test = TrainTestSplit(ratio=0.8, shuffle=False).split(data)

    learner = GrpcLearner.with_address(address="localhost:8080")
    # .run_docker(
    #    image="collaborating.tuhh.de:5005/w-6/agenc/agenc/java-automata-learner:latest",
    # )
    inputs = [
        "i0",
        "o0",
        "i1",
        "o1",
        "i2",
        "o2",
        "i3",
        "o3",
        "i4",
        "o4",
        "i5",
        "o5",
        "i6",
        "o6",
        "i7",
        "o7",
        "i8",
        "o8",
        "i9",
        "o9",
        "i10",
        "o10",
        "i11",
        "o11",
        "i12",
        "o12",
        "i13",
        "o13",
        "i14",
        "o14",
        "i15",
        "o15",
        "i16",
        "o16",
        "i17",
        "o17",
        "i18",
        "o18",
        "i19",
    ]
    outputs = ["o19"]

    model = learn_offline(
        train,
        learner,
        inputs,
        outputs,
    )

    report = evaluate_offline(
        model,
        test,
        inputs,
        outputs,
        [MeanAbsoluteError(), MeanSquaredError()],
    )
    print(report)


if __name__ == "__main__":
    main()
