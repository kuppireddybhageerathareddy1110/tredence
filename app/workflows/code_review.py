from typing import Dict, Any
from app.engine import Graph
from app.tools import TOOLS


# ---------------------------
# Node functions
# ---------------------------

def extract_functions(state: Dict[str, Any]):
    code = state.get("code", "")
    # trivial extraction: treat any block containing "def " as a function
    funcs = [part for part in code.split("\n\n") if "def " in part][:10]
    state["functions"] = funcs
    return {"extracted": len(funcs)}


def check_complexity(state: Dict[str, Any]):
    funcs = state.get("functions", [])
    scores = []

    for f in funcs:
        r = TOOLS["measure_complexity"](f)
        scores.append(r["score"])

    avg = sum(scores) / len(scores) if scores else 0
    state["avg_complexity"] = avg
    return {"avg_complexity": avg}


def detect_issues(state: Dict[str, Any]):
    funcs = state.get("functions", [])
    total_issues = 0

    for f in funcs:
        r = TOOLS["detect_smells"](f)
        total_issues += r["issues"]

    state["issues"] = total_issues
    return {"issues": total_issues}


def suggest_improvements(state: Dict[str, Any]):
    issues = state.get("issues", 0)
    complexity = state.get("avg_complexity", 0)

    score = max(0, 100 - issues * 10 - complexity * 5)
    state["quality_score"] = score

    suggestions = []

    if issues > 0:
        suggestions.append("Reduce prints and TODOs")

    if complexity > 5:
        suggestions.append("Refactor large functions into smaller helpers")

    state["suggestions"] = suggestions
    return {"quality_score": score}


# ---------------------------
# Graph builder
# ---------------------------

def build_code_review_graph(graph_id: str, threshold: float = 80.0) -> Graph:
    g = Graph(graph_id)

    g.add_node("extract", extract_functions)
    g.add_node("complexity", check_complexity)
    g.add_node("detect", detect_issues)
    g.add_node("suggest", suggest_improvements)

    g.add_edge("extract", "complexity")
    g.add_edge("complexity", "detect")
    g.add_edge("detect", "suggest")

    # conditional looping logic
    def chooser(state: Dict[str, Any]):
        score = state.get("quality_score", 0)

        if score >= threshold:
            return None  # stop workflow

        # limit looping to avoid infinite cycles
        state.setdefault("_loop_count", 0)
        state["_loop_count"] += 1

        if state["_loop_count"] > 5:
            return None  # stop after 5 loops max

        return "extract"  # loop back

    g.add_conditional("suggest", chooser)
    return g
