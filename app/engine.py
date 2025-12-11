from typing import Callable, Dict, Any, Optional, List
from pydantic import BaseModel
import asyncio

NodeFn = Callable[[Dict[str, Any]], Any]


class Node:
    def __init__(self, name: str, func: NodeFn, is_async: bool = False):
        self.name = name
        self.func = func
        self.is_async = is_async


class Graph:
    def __init__(self, graph_id: str):
        self.id = graph_id
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, List[str]] = {}
        self.conditional_routes: Dict[str, Callable[[Dict[str, Any]], Optional[str]]] = {}

    def add_node(self, name: str, func: NodeFn, is_async: bool = False):
        self.nodes[name] = Node(name, func, is_async)

    def add_edge(self, src: str, dst: str):
        self.edges.setdefault(src, []).append(dst)

    def add_conditional(self, src: str, chooser: Callable[[Dict[str, Any]], Optional[str]]):
        # chooser returns next node name or None
        self.conditional_routes[src] = chooser


class Runner:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.log: List[str] = []

    async def run_node(self, node: Node, state: Dict[str, Any]):
        self.log.append(f"ENTER {node.name}: state snapshot: {state}")

        if node.is_async:
            result = await node.func(state)
        else:
            # run sync function in threadpool
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(None, node.func, state)

        self.log.append(f"EXIT {node.name}: produced: {result}")
        return result

    async def run(self, start: str, state: Dict[str, Any], max_steps: int = 1000):
        current = start
        steps = 0

        while current is not None and steps < max_steps:
            steps += 1

            if current not in self.graph.nodes:
                self.log.append(f"ERROR: node {current} not found")
                break

            node = self.graph.nodes[current]
            await self.run_node(node, state)

            # conditional routing takes priority
            if current in self.graph.conditional_routes:
                chooser = self.graph.conditional_routes[current]
                next_node = chooser(state)
                self.log.append(f"CHOICE from {current} -> {next_node}")
                current = next_node
                continue

            # follow edges (only first edge)
            next_nodes = self.graph.edges.get(current, [])
            if not next_nodes:
                current = None
            else:
                current = next_nodes[0]

        if steps >= max_steps:
            self.log.append("WARN: reached max_steps")

        return state, self.log
