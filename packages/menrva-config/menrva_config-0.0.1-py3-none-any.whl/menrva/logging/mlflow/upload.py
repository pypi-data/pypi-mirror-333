"""
Upload a file or folder on an MLFlow run
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from . import identifier_to_run_id

import argparse

from mlflow.tracking import MlflowClient
import urllib3
import warnings

if __name__ == "__main__":
    # warnings
    urllib3.disable_warnings()
    warnings.simplefilter("ignore", UserWarning)

    parser = argparse.ArgumentParser("MLFlow Upload file")
    parser.add_argument(
        "run_id", type=str, help="uuid or identifier of the run to download"
    )
    parser.add_argument("path", type=str, help="local path to upload")
    parser.add_argument("--dir-to", type=str, default=None, help="remote directory")
    parser.add_argument("--tracking-uri", type=str, help="MLFlow tracking uri")
    parser.add_argument("--registry-uri", type=str, help="MLFlow registry uri")
    parser.add_argument("--override", action="store_true", help="override if exists")
    args = parser.parse_args()

    uuid = identifier_to_run_id(args.run_id)

    client = MlflowClient(
        tracking_uri=args.tracking_uri, registry_uri=args.registry_uri
    )

    if (
        Path(args.path).name
        in [Path(p.path).name for p in client.list_artifacts(uuid, args.dir_to)]
        and not args.override
    ):
        print("file exists on server, override with --override", file=sys.stderr)
        sys.exit(1)
    else:
        client.log_artifact(uuid, args.path, args.dir_to)
