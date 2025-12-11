from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from uuid import uuid4
import asyncio
import uvicorn

from app.schemas import GraphCreate, RunCreate
from app.storage import save_graph, get_graph, new_run, update_run, get_run
from app.workflows.code_review import build_code_review_graph
from app.engine import Runner


app = FastAPI(title="Minimal Workflow Engine")


# ---------------------------
# Root Route (Fixes 404)
# ---------------------------
@app.get("/")
def root():
    return {"message": "Workflow engine running", "docs": "/docs"}


# ---------------------------
# Create Graph
# ---------------------------
@app.post("/graph/create")
def create_graph(payload: GraphCreate):
    graph_id = payload.graph_id or f"graph_{str(uuid4())[:8]}"

    # Only one built-in workflow type for now
    if payload.type == "code_review":
        threshold = float(payload.params.get("threshold", 80.0))
        g = build_code_review_graph(graph_id, threshold=threshold)
        save_graph(g)
        return {"graph_id": graph_id}

    return {"error": "unknown graph type"}


# ---------------------------
# Run Graph Workflow
# ---------------------------
@app.post("/graph/run")
async def run_graph(payload: RunCreate, background_tasks: BackgroundTasks):
    graph = get_graph(payload.graph_id)
    if graph is None:
        return {"error": "graph not found"}

    run_id = new_run(payload.graph_id, payload.initial_state)
    runner = Runner(graph)

    async def _execute():
        state, logs = await runner.run(
            start=list(graph.nodes.keys())[0],
            state=payload.initial_state
        )
        update_run(run_id, state, logs, status="finished")

    # Correct background execution
    background_tasks.add_task(lambda: asyncio.run(_execute()))

    return {"run_id": run_id}


# ---------------------------
# Get State of a Run
# ---------------------------
@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    r = get_run(run_id)
    if not r:
        return {"error": "run not found"}

    return {"state": r["state"], "log": r["log"], "status": r["status"]}


# ---------------------------
# WebSocket for Live Logs
# ---------------------------
@app.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await websocket.accept()

    try:
        while True:
            r = get_run(run_id)
            if not r:
                await websocket.send_json({"error": "run not found"})
                break

            await websocket.send_json({
                "state": r["state"],
                "log": r["log"],
                "status": r["status"]
            })

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass


# ---------------------------
# Application Entry Point
# ---------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
