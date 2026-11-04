from orgalego.core.modeling.node import Node
from orgalego.core.modeling.edge import Edge


def merged_pairs(graph: "OrgGraph") -> dict[tuple[str, str], float]:

    merged: dict[tuple[str, str], float] = {}
    for edge in graph.edges:
        key = tuple(sorted((edge.source, edge.target)))
        merged[key] = merged.get(key, 0.0) + edge.weight
    return merged


class OrgGraph:

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []
        self.adjacency: dict[str, list[tuple[str, float]]] = {}

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def add_node(self, node: Node) -> None:

        if node.id in self.nodes:
            raise ValueError(f"Node '{node.id}' already exists.")
        self.nodes[node.id] = node
        self.adjacency.setdefault(node.id, [])

    def add_edge(self, edge=None, target=None, *, weight=1.0, directed=False) -> None:

        if not isinstance(edge, Edge):
            edge = Edge(source=edge, target=target, weight=weight,
                        directed=directed)

        if edge.source not in self.nodes:
            raise ValueError(f"Edge to unknown node: '{edge.source}'.")
        if edge.target not in self.nodes:
            raise ValueError(f"Edge to unknown node: '{edge.target}'.")

        self.edges.append(edge)
        self.adjacency[edge.source].append((edge.target, edge.weight))
        if not edge.directed:
            self.adjacency[edge.target].append((edge.source, edge.weight))

    def remove_node(self, node_id) -> None:

        if node_id not in self.nodes:
            raise ValueError(f"Unknown node: '{node_id}'.")
        del self.nodes[node_id]
        self.edges = [e for e in self.edges
                      if e.source != node_id and e.target != node_id]
        # Rebuild the adjacency from scratch to stay consistent.
        self.adjacency = {nid: [] for nid in self.nodes}
        kept = self.edges
        self.edges = []
        for e in kept:
            self.add_edge(e)

    # ------------------------------------------------------------------
    # Basic access
    # ------------------------------------------------------------------

    def neighbors(self, node_id: str) -> list[tuple[str, float]]:
        return self.adjacency.get(node_id, [])

    def node_ids(self) -> list[str]:
        return list(self.nodes.keys())

    def workload(self, node_id: str) -> float:

        total = 0.0
        for e in self.edges:
            if e.target == node_id or (not e.directed and e.source == node_id):
                total += e.weight
        return round(total, 3)

    def total_weight(self) -> float:
        return round(sum(edge.weight for edge in self.edges), 4)

    def __len__(self) -> int:
        return len(self.nodes)

    def copy(self) -> "OrgGraph":

        g = OrgGraph()
        for node in self.nodes.values():
            g.add_node(node)
        for e in self.edges:
            g.add_edge(Edge(e.source, e.target, e.weight, e.directed))
        return g

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:

        problems: list[str] = []

        for nid, node in self.nodes.items():
            if not (0 <= node.rank <= 10):
                problems.append(f"Node '{nid}': invalid rank ({node.rank}).")

        for nid in self.nodes:
            if not self.adjacency.get(nid):
                has_incoming = any(
                    t == nid for u in self.adjacency for (t, _) in self.adjacency[u]
                )
                if not has_incoming:
                    problems.append(f"Isolated node (no edge): '{nid}'.")

        return problems

    # ------------------------------------------------------------------
    # Projections by rank band
    # ------------------------------------------------------------------

    def get_band_nodes(self, band: str) -> list[str]:
        return [nid for nid, node in self.nodes.items() if node.band == band]

    def as_merged_undirected(self) -> "OrgGraph":

        g = OrgGraph()
        for node in self.nodes.values():
            g.add_node(node)
        for (u, v), weight in merged_pairs(self).items():
            g.add_edge(Edge(source=u, target=v, weight=weight, directed=False))
        return g
