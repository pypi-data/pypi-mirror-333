import mlflow
from mlflow.entities import Run
import logging
import re
from menrva.logging import create_identifier
from typing import List, Optional, Callable, Literal, Union
from mlflow.utils.mlflow_tags import MLFLOW_PARENT_RUN_ID
import numpy as np
import pandas as pd

_logger = logging.getLogger(__name__)

__all__ = [
    "assign_identifier",
    "get_run_by_identifier",
    "identifier_to_run_id",
    "get_children_runs",
    "compare_runs_by_param",
    "metrics_from_runs",
]

# Things to implement
# 1. load from config
# 2. log configuration
# 4. create module to overwrite the commit on mlflow

## Identifier functions


def assign_identifier(run_id: str):
    """
    Assign a unique identifier to a run creating a tag identifier
    """
    run = mlflow.get_run(run_id)
    if "identifier" in run.data.tags:
        curr_identifier = run.data.tags["identifier"]
        _logger.warn(
            f"run {run.info.run_id} already have an identifier {curr_identifier}, no op."
        )
    else:
        client = mlflow.tracking.MlflowClient()
        client.set_tag(run_id, "identifier", new_id := create_identifier())
        _logger.info(f"run {run.info.run_id} with identifier {new_id}")


def get_run_by_identifier(run_identifier: str) -> Run:
    """
    Returns a Run object searching for the tag identifier, throws an error
    if no run or multiple ones are found.
    """
    identifier_pattern = (
        "[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+"
    )
    if re.search(identifier_pattern, run_identifier):
        all_exps = [e.experiment_id for e in mlflow.search_experiments()]
        run = mlflow.search_runs(all_exps, f"tags.identifier = '{run_identifier}'")
        if len(run) == 0:
            raise ValueError(f"Run with identifier {run_identifier}")
        elif len(run) > 1:
            raise RuntimeError(f"Multiple runs with identifier {run_identifier} found")
        return mlflow.get_run(run["run_id"][0])
    else:
        return mlflow.get_run(run_identifier)


def identifier_to_run_id(mlflow_uri: str) -> str:
    """
    Takes in input a mlflow artifact uri or mlflow model, run uri and translate
    the identifier into the correct run id. In this way you can abstract from
    the mlflow specific run id.

    .. note ::
        if the mlflow_uri does not contain the identifier it just returns it
    """
    identifier_pattern = (
        "[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+"
    )
    if ident := re.search(identifier_pattern, mlflow_uri):
        run_id = get_run_by_identifier(ident.group()).info.run_id
        mlflow_uri = re.sub(identifier_pattern, run_id, mlflow_uri)
    return mlflow_uri


## Utility Functions


def get_children_runs(run_id: str) -> List[Run]:
    """
    Returns the children runs of the specified run
    """

    if "-" in run_id:
        run_id = get_run_by_identifier(run_id).info.run_id

    all_exps = [e.experiment_id for e in mlflow.search_experiments()]
    runs = mlflow.search_runs(all_exps, f"tags.`{MLFLOW_PARENT_RUN_ID}` = '{run_id}'")
    if len(runs) == 0:
        raise ValueError(f"run {run_id} doesn't have children runs")
    return [mlflow.get_run(id) for id in runs["run_id"] if id != run_id]


def compare_runs_by_param(
    param: str,
    metrics: List[str],
    *,
    container: Optional[str] = None,
    other_runs: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Takes a container run and optionally a set of other runs, and compares a
    set of metrics by the specificed parameter
    """
    runs = []
    if container is not None:
        runs = get_children_runs(get_run_by_identifier(container).info.run_id)
    if other_runs is not None:
        runs.extend(
            [
                get_run_by_identifier(other) if "-" in other else mlflow.get_run(other)
                for other in other_runs
            ]
        )
    param_values = np.array(r.data.params[param] for r in runs)
    metrics = {
        m: np.array([r.data.metrics.get(m, None) for r in runs]) for m in metrics
    }
    out = pd.DataFrame({param: param_values} | metrics)
    return out


def metrics_from_runs(
    runs: List[str],
    metrics: List[str],
    *,
    index: Union[
        Literal["parent", "run_name", "run_id"], Callable[[Run], str]
    ] = "run_id",
    cols_rename: Callable = lambda x: x,
):
    """
    Takes a set of runs and metrics and generates a table containing a row for
    each run with its metrics. By default each run index is its run_id but it
    can be overrided with the parent run name.
    """

    # accumulate runs
    results = {}
    for run_id in map(identifier_to_run_id, runs):
        if index == "parent":
            used_name = mlflow.get_parent_run(run_id).data.tags["mlflow.runName"]
        elif index == "run_name":
            used_name = mlflow.get_run(run_id).data.tags["mlflow.runName"]
        elif index == "run_id":
            used_name = mlflow.get_run(run_id).info.run_id
        else:
            used_name = index(mlflow.get_run(run_id))
        results[used_name] = mlflow.get_run(run_id).data.metrics

    table = pd.DataFrame.from_dict(results).T

    # filter metrics and rename
    if isinstance(metrics, (list, tuple)):
        table = table[metrics]
    else:
        used_cols = {}
        for col in table.columns:
            if group := re.match(metrics, col):
                if group.groups():
                    used_cols[col] = ",".join(group.groups())
                else:
                    used_cols[col] = group.group()
        table = table[used_cols.keys()].rename(columns=used_cols)

    # rename indexes
    table = table.rename(columns=cols_rename)

    return table
