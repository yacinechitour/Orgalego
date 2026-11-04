from orgalego.core.modeling.graph import OrgGraph, merged_pairs
from orgalego.core.modeling.edge import Edge



class UnionFind:

    def __init__(self, elements: list[str]) -> None:
        self.parent: dict[str, str] = {e: e for e in elements}
        self.rank: dict[str, int] = {e: 0 for e in elements}

    def find(self, x: str) -> str:
        
        if self.parent[x] != x: self.parent[x] = self.find(self.parent[x])
        
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:

        rx, ry = self.find(x), self.find(y)
        
        if rx == ry: return False
        
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        
        if self.rank[rx] == self.rank[ry] : self.rank[rx] += 1
        return True



def kruskal(graph: OrgGraph) -> OrgGraph:
    
    mst = OrgGraph()
    uf = UnionFind(graph.node_ids())
    edges = sorted((w, u, v) for (u, v), w in merged_pairs(graph).items())

    for node in graph.nodes.values(): mst.add_node(node)

    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.add_edge(Edge(
                source=u,
                target=v,
                weight=round(weight, 2),
                directed=False
            ))

    return mst
