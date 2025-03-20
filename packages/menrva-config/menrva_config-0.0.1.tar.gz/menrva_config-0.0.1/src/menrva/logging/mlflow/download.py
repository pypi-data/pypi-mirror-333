"""
Downloads from mlflow an experiment
"""

import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from . import identifier_to_run_id

import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME
import urllib3
import warnings

if __name__ == "__main__":
    # warnings
    urllib3.disable_warnings()
    warnings.simplefilter("ignore", UserWarning)

    # arguments parser
    parser = argparse.ArgumentParser(
        "MLFlow Tracking downloader, downloads an MLFlow run provided its uuid"
    )
    parser.add_argument(
        "uuid",
        type=str,
        help="uuid or identifier of the run to download",
    )
    parser.add_argument(
        "--out",
        "-o",
        type=Path,
        default=Path.cwd() / "experiments",
        help="folder in which save the run data",
    )
    parser.add_argument(
        "--by-name", action="store_true", help="use the name of the run instead of UUID"
    )
    parser.add_argument("--tracking-uri", type=str, help="MLFlow tracking uri")
    parser.add_argument("--registry-uri", type=str, help="MLFlow registry uri")
    args = parser.parse_args()

    # set uri
    if args.tracking_uri:
        mlflow.set_tracking_uri(args.tracking_uri)
    if args.registry_uri:
        mlflow.set_registry_uri(args.registry_uri)

    run_name = args.uuid
    args.uuid = identifier_to_run_id(args.uuid)
    if args.by_name:
        run = mlflow.get_run(args.uuid)
        run_name = run.data.tags.get(MLFLOW_RUN_NAME, run_name)

    out_path: Path = args.out / run_name if args.out.exists() else args.out
    out_path.mkdir(exist_ok=True, parents=True)
    mlflow.artifacts.download_artifacts(run_id=args.uuid, dst_path=out_path)
