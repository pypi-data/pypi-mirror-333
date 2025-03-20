"""
Generates the html diff among two files on mlflow
"""

import difflib
from argparse import ArgumentParser
from pathlib import Path

import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from . import identifier_to_run_id


import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME

import urllib3
import warnings


def save_html_diff(file1: Path, name1: str, file2: Path, name2: str, output: Path):
    lines1 = open(file1).readlines()
    lines2 = open(file2).readlines()
    delta = difflib.HtmlDiff().make_file(lines1, lines2, name1, name2)
    with open(output, "w") as f:
        f.write(delta)


if __name__ == "__main__":
    # warnings
    urllib3.disable_warnings()
    warnings.simplefilter("ignore", UserWarning)

    parser = ArgumentParser("HTML Diff among MLFlow files")
    parser.add_argument("uuid1", type=str, help="uuid or identifier 1")
    parser.add_argument("path1", type=str, help="path to compare 1")
    parser.add_argument("uuid2", type=str, help="uuid or identifier 2")
    parser.add_argument("path2", type=str, help="path to compare 2")
    parser.add_argument("--out", "-o", type=Path, default=Path.cwd() / "diff.html")
    parser.add_argument("--tracking-uri", type=str, help="MLFlow tracking uri")
    parser.add_argument("--registry-uri", type=str, help="MLFlow registry uri")
    args = parser.parse_args()

    uuid_1 = identifier_to_run_id(args.uuid1)
    run_1 = mlflow.get_run(uuid_1)
    name_1 = run_1.data.tags.get(MLFLOW_RUN_NAME, uuid_1)
    path_1 = args.path1

    uuid_2 = identifier_to_run_id(args.uuid2)
    run_2 = mlflow.get_run(uuid_2)
    name_2 = run_2.data.tags.get(MLFLOW_RUN_NAME, uuid_2)
    path_2 = args.path2

    file_1 = Path(
        mlflow.artifacts.download_artifacts(run_id=uuid_1, artifact_path=path_1)
    )
    file_2 = Path(
        mlflow.artifacts.download_artifacts(run_id=uuid_2, artifact_path=path_2)
    )
    save_html_diff(
        file_1, name_1 + "/" + file_1.name, file_2, name_2 + "/" + file_2.name, args.out
    )
