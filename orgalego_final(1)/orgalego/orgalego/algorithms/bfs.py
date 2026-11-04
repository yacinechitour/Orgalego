from collections import deque

from orgalego.core.modeling.graph import OrgGraph
from orgalego.algorithms import reconstruct_path


class BFSResult:

    def __init__(self, source: str):
        self.source = source
        self.distances: dict[str, int] = {}
        self.parents: dict[str, str | None] = {}

    def path_to(self, target: str) -> list[str] | None:

        if target not in self.distances:
            return None

        return reconstruct_path(self.parents, target)


def bfs(graph: OrgGraph, source: str) -> BFSResult:

    if source not in graph.nodes:
        raise ValueError(f"Unknown source: '{source}'.")

    result = BFSResult(source=source)
    result.distances[source] = 0
    result.parents[source] = None

    queue: deque[str] = deque([source])
    
    while queue:

        u = queue.popleft()
        du = result.distances[u]

        for (v, _cost) in graph.neighbors(u):
            if v not in result.distances: 
                result.distances[v] = du + 1
                result.parents[v] = u
                queue.append(v)

    return result


def hierarchical_distance(graph: OrgGraph, source: str, target: str) -> int | None:
    
    return bfs(graph, source).distances.get(target)
