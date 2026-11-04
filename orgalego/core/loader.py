import json

from orgalego.core.modeling.node import Node
from orgalego.core.modeling.edge import Edge
from orgalego.core.modeling.graph import OrgGraph


def load_graph(path: str) -> OrgGraph:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return build_graph(data)


def build_graph(data: dict) -> OrgGraph:
    graph = OrgGraph()

    for n in data.get("nodes", []):
        graph.add_node(Node(
            id=str(n["id"]),
            label=n.get("label", str(n["id"])),
            rank=float(n["rank"]),
            node_type=n.get("type", "entity"),
            group_key=n.get("group_key"),
            unit_axis=n.get("unit_axis", ""),
            financial_flow=float(n.get("financial_flow", 0.0)),
            attributes=dict(n.get("attributes", {}) or {}),
            role_family=n.get("role_family", ""),
            role_title=n.get("role_title", ""),
        ))

    for e in data.get("edges", []):
        graph.add_edge(Edge(
            source=str(e["source"]),
            target=str(e["target"]),
            weight=float(e.get("weight", 1.0)),
            directed=bool(e.get("directed", False)),
        ))


    for nid, node in graph.nodes.items():
        node.workload = graph.workload(nid)

    return graph
