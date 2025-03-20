from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Callable, Coroutine, List

from typing_extensions import TypeVar


class Graphable(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

T = TypeVar('T', bound='Graphable')


class Node:
    def __init__(self, ref: T, graph: Graph):
        self.ref: T = ref
        self.graph: Graph = graph

    def get_ref(self) -> T:
        return self.ref


class Edge:
    def __init__(self, a: Node, b: Node):
        self.a = a
        self.b = b

        self.properties = {}

    def get_a(self) -> T:
        return self.a.get_ref()

    def get_b(self) -> T:
        return self.b.get_ref()

    def get_other(self, me: T) -> T:
        if self.get_a() == me: return self.get_b()
        if self.get_b() == me: return self.get_a()

    def is_member(self, me: T) -> bool:
        if self.get_a() == me: return True
        if self.get_b() == me: return True

        return False

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value


class Graph:
    def __init__(self):
        self.node_added_listeners = []
        self.edge_added_listeners = []

        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}

        self.properties = {}

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, key, value):
        self.properties[key] = value

    def add_node_added_listener(self, fn: Callable[[Node], Coroutine]):
        self.node_added_listeners.append(fn)

    def add_edge_added_listener(self, fn: Callable[[Edge], Coroutine]):
        self.edge_added_listeners.append(fn)

    async def on_node_added(self, node: Node):
        await asyncio.gather(*[listener(node) for listener in self.node_added_listeners])

    async def on_edge_added(self, edge: Edge):
        await asyncio.gather(*[listener(edge) for listener in self.edge_added_listeners])

    async def add_node(self, ref: T):
        if ref.get_id() in self.nodes: return

        self.nodes[ref.get_id()] = Node(ref, self)
        await self.on_node_added(self.nodes[ref.get_id()])

    def get_node(self, ref_id: str) -> Node:
        return self.nodes.get(ref_id, None)

    def get_nodes(self):
        return list(self.nodes.values())

    async def add_edge(self, a: T, b: T):
        key = (a.get_id(), b.get_id())
        if key in self.edges: return
        if (b.get_id(), a.get_id()) in self.edges: return

        node_a = self.get_node(a.get_id())
        node_b = self.get_node(b.get_id())

        self.edges[key] = Edge(node_a, node_b)
        await self.on_edge_added(self.edges[key])

    def _add_edge(self, a: Node, b: Node):
        self.edges[(a.ref.get_id(), b.ref.get_id())] = Edge(a, b)

    def get_edge(self, a: T, b: T) -> Edge:
        return self.edges.get((a.get_id(), b.get_id()), None)

    def _get_edge(self, a: Node, b: Node) -> Edge:
        return self.edges.get((a.ref.get_id(), b.ref.get_id()), None)

    def get_edges(self, fn: Callable[[Edge], bool] = None) -> List[Edge]:
        fn = fn if fn else lambda e: True
        return [edge for edge in self.edges.values() if fn(edge)]
