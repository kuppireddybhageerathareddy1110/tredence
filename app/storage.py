import uuid
from typing import Dict, Any
from app.engine import Graph


# In-memory storage for graphs and runs
GRAPHS: Dict[str, Graph] = {}
RUNS: Dict[str, Dict[str, Any]] = {}


def save_graph(graph: Graph):
    GRAPHS[graph.id] = graph


def get_graph(graph_id: str) -> Graph:
    return GRAPHS.get(graph_id)


def new_run(graph_id: str, initial_state: Dict[str, Any]) -> str:
    run_id = str(uuid.uuid4())
    RUNS[run_id] = {
        "graph_id": graph_id,
        "state": initial_state,
        "log": [],
        "status": "running"
    }
    return run_id


def update_run(run_id: str, state: Dict[str, Any], log: list, status: str = None):
    if run_id in RUNS:
        RUNS[run_id]["state"] = state
        RUNS[run_id]["log"] = log
        if status:
            RUNS[run_id]["status"] = status


def get_run(run_id: str):
    return RUNS.get(run_id)
