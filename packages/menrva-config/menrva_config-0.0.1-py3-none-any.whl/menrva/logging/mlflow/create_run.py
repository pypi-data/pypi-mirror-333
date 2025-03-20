"""
Creates a run and returns it's run_id
it is useful to create a container with metadata
for other runs or a run simply storing artifacts and 
meta data
"""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from . import identifier_to_run_id

import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID
import argparse
import os
from uuid import uuid4
import urllib3
import warnings


if __name__ == "__main__":
    # warnings
    urllib3.disable_warnings()
    warnings.simplefilter("ignore", UserWarning)

    parser = argparse.ArgumentParser("Creates and empty run to contain others")
    parser.add_argument("run_name", type=str, help="RUN NAME")
    parser.add_argument(
        "--experiment",
        type=str,
        default=os.environ["MLFLOW_EXPERIMENT_NAME"]
        if "MLFLOW_EXPERIMENT_NAME" in os.environ
        else None,
        help="experiment name",
    )
    parser.add_argument("--type", type=str, help="type of run")
    parser.add_argument(
        "--parent", type=identifier_to_run_id, help="run_id of ther parent run"
    )
    parser.add_argument("--artifacts", type=Path, help="artifacts to be stored")
    args = parser.parse_args()

    client = mlflow.tracking.MlflowClient()
    tags = {"identifier": str(uuid4())}
    if args.type is not None:
        tags["type"] = args.type
    if args.parent is not None:
        tags[MLFLOW_PARENT_RUN_ID] = args.parent

    exp_name = os.environ.get("MLFLOW_EXPERIMENT_NAME", None)
    if args.experiment is not None:
        exp_name = args.experiment
    if exp_name is None:
        print(
            "either MLFLOW_EXPERIMENT_NAME setted or --experiment used", file=sys.stderr
        )
        sys.exit(1)

    run = client.create_run(
        experiment_id=mlflow.get_experiment_by_name(exp_name).experiment_id,
        run_name=args.run_name,
        tags=tags,
    )
    if args.artifacts is not None:
        artifacts: Path = args.artifacts
        if artifacts.exists():
            if artifacts.is_dir():
                client.log_artifacts(run.info.run_id, str(artifacts))
            else:
                client.log_artifact(run.info.run_id, str(artifacts))
        else:
            print(f"path {artifacts} does not exist, not uploading")

    client.set_terminated(run.info.run_id, "FINISHED")
    print(tags["identifier"])
