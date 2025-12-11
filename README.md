
---

# **Minimal Workflow Engine (FastAPI) — AI Engineering Internship Assignment**

This repository implements a **minimal agent workflow engine** inspired by LangGraph concepts.
It demonstrates a clear understanding of **Python backend development**, **async programming**, **API design**, and **workflow orchestration** — as required for the AI Engineering Internship assignment.

This project is intentionally simple, clean, and modular, focusing on **correctness**, **clarity**, and **architecture**, rather than features or UI.

---

# **1. Project Overview**

This backend system allows you to:

* Define a workflow as a set of **nodes** (Python functions).
* Link them using **edges**.
* Maintain a shared **mutable state** flowing through nodes.
* Support **branching**, **conditional routing**, and **looping logic**.
* Execute workflows asynchronously.
* Expose the entire engine via **FastAPI endpoints**.
* Inspect workflow run state and execution logs.

No frontend, machine learning, or external deployment is required.

---

# **2. Features**

### ✔ **Nodes**

Each node is a Python function:

```python
def extract(state):
    state["x"] = ...
    return {"info": ...}
```

Nodes **read and modify** a shared `state` dictionary.

---

### ✔ **State**

* A Python `dict` that flows through the graph.
* Nodes add/update keys.
* Final state is returned at the end of execution.

---

### ✔ **Edges**

Defines execution flow:

```
extract → complexity → detect → suggest
```

---

### ✔ **Branching**

Nodes may decide the next node dynamically.

---

### ✔ **Looping**

Workflows can repeat nodes until a condition is satisfied.

Example:
Loop until `quality_score >= threshold`.

---

### ✔ **Tool Registry**

A simple global dictionary for reusable helper functions:

```python
TOOLS["detect_smells"](code)
```

---

### ✔ **FastAPI Endpoints**

| Method | Endpoint                | Purpose                           |
| ------ | ----------------------- | --------------------------------- |
| POST   | `/graph/create`         | Create a new workflow graph       |
| POST   | `/graph/run`            | Run a graph with an initial state |
| GET    | `/graph/state/{run_id}` | Fetch execution state + logs      |
| WS     | `/ws/{run_id}`          | Stream state/logs live (optional) |

---

### ✔ **Background Execution**

Workflows run asynchronously so the API stays responsive.

---

### ✔ **Example Workflow Implemented**

**Option A — Code Review Mini-Agent**

1. Extract functions
2. Measure complexity
3. Detect issues
4. Suggest improvements
5. Loop until quality score meets threshold

This meets the assignment requirements.

---

# **3. Project Structure**

```
fastapi-workflow-engine/
├─ app/
│  ├─ main.py                # FastAPI app + endpoints
│  ├─ engine.py              # Core engine: Node, Graph, Runner
│  ├─ tools.py               # Tool registry + helper functions
│  ├─ workflows/
│  │  └─ code_review.py      # Code Review mini-agent workflow
│  ├─ storage.py             # In-memory storage for graphs & runs
│  └─ schemas.py             # Pydantic request models
└─ README.md
```

---

# **4. Installation & Setup**

### **Step 1 — Clone the repository**

```bash
git clone https://github.com/kuppireddybhageerathareddy1110/tredence.git
cd fastapi-workflow-engine
```

### **Step 2 — Create and activate a virtual environment**

Windows PowerShell:

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

Linux / macOS / WSL:

```bash
python3 -m venv env
source env/bin/activate
```

### **Step 3 — Install dependencies**

```bash
pip install fastapi uvicorn pydantic
```

### **Step 4 — Run the FastAPI server**

```bash
uvicorn app.main:app --reload --port 8000
```

Open Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# **5. How the Workflow Engine Works**

## **5.1 Define Graph**

A graph is built using:

```python
g.add_node("extract", extract_functions)
g.add_edge("extract", "complexity")
g.add_conditional("suggest", chooser)
```

Nodes execute in order, modifying the shared state.

---

## **5.2 Runner**

The `Runner` class executes a workflow:

* Logs every step
* Supports async node execution
* Supports looping with `chooser()`
* Stops when a node returns `None` as next step

---

## **5.3 Example — Code Review Workflow**

### State input:

```json
{
  "code": "def hello(): print('test') # TODO: improve"
}
```

### Workflow steps:

| Step       | Description                          |
| ---------- | ------------------------------------ |
| extract    | Finds functions                      |
| complexity | Calculates complexity score          |
| detect     | Detects smells like prints or TODO   |
| suggest    | Computes quality score + suggestions |
| loop       | If score < threshold → repeat        |

### Final Output Example:

```json
{
  "quality_score": 84.9,
  "suggestions": ["Reduce prints and TODOs"]
}
```

---

# **6. API Usage Examples**

## **6.1 Create a graph**

POST → `/graph/create`

```json
{
  "type": "code_review",
  "params": {"threshold": 80}
}
```

Response:

```json
{"graph_id": "graph_12345"}
```

---

## **6.2 Run a graph**

POST → `/graph/run`

```json
{
  "graph_id": "graph_12345",
  "initial_state": {
    "code": "def hello(): print('hi') # TODO fix"
  }
}
```

Response:

```json
{"run_id": "9ab3d2..."}
```

---

## **6.3 Check run status**

GET → `/graph/state/{run_id}`

Returns:

* state
* logs
* status (`running` or `finished`)

---

## **6.4 WebSocket stream**

```
ws://127.0.0.1:8000/ws/{run_id}
```

Streams execution every second.

---

# **7. What This Engine Supports**

* Node execution (sync + async)
* State mutation and transfer
* Deterministic workflow graphs
* Conditional branching and looping
* Simple tool registry
* Background workflow execution
* State + log retrieval
* Optional WebSocket live updates

---

# **8. Possible Improvements (If More Time Was Available)**

### 1. **Persistent storage (SQLite/Postgres)**

Store graphs and run logs permanently.

### 2. **Dynamic graph creation**

Allow adding custom nodes via the API.

### 3. **Parallel branching (fan-out / fan-in)**

Execute nodes concurrently.

### 4. **Workflow visualization UI**

(Not required, but useful for debugging.)

### 5. **Node execution timeouts & retries**

More robust workflow execution.

### 6. **Role-based access control**

Secure API usage in multi-user environments.

### 7. **Unit tests**

Automate testing for the engine and API.

---

# **9. Conclusion**

This project provides a clean, correct, and extensible implementation of the assignment requirements:

* Minimal graph engine
* Tool registry
* Async execution
* FastAPI endpoints
* Example workflow demonstrating loops, branching, and state mutation

The codebase is modular, readable, and production-style, reflecting good backend engineering practices.

---

# **Author**

**Kuppireddy Bhageeratha Reddy**

---


