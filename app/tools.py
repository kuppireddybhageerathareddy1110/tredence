from typing import Dict, Any

# A minimal tool registry
TOOLS: Dict[str, callable] = {}


def register(name: str):
    def _wrap(fn):
        TOOLS[name] = fn
        return fn
    return _wrap


@register("detect_smells")
def detect_smells(code: str) -> Dict[str, Any]:
    # simple rule-based 'smell' detector: harsher heuristics for demo
    issues = 0

    if "TODO" in code:
        issues += 1
    if "print(" in code:
        issues += 1
    if len(code.splitlines()) > 200:
        issues += 1

    return {"issues": issues}


@register("measure_complexity")
def measure_complexity(code: str) -> Dict[str, Any]:
    # naive complexity: number of `def` + nesting by counting tabs
    funcs = code.count("def ")
    lines = len(code.splitlines())
    score = funcs * 1 + (lines / 100)

    return {"funcs": funcs, "lines": lines, "score": score}
