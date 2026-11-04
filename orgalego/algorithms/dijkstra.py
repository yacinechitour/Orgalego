import heapq
import math

from orgalego.core.modeling.graph import OrgGraph
from orgalego.algorithms import reconstruct_path


class DijkstraResult:

    def __init__(self, source: str):
        self.source = source
        self.distances: dict[str, float] = {}
        self.parents: dict[str, str | None] = {}

    def path_to(self, target: str) -> list[str] | None:
        """Rebuild the shortest path from the source to target."""
        if self.distances.get(target, math.inf) == math.inf:
            return None
        return reconstruct_path(self.parents, target)


def dijkstra(graph: OrgGraph, source: str) -> DijkstraResult:

    if source not in graph.nodes:
        raise ValueError(f"Unknown source: '{source}'.")

    result = DijkstraResult(source=source)
    for nid in graph.node_ids():
        result.distances[nid] = math.inf
        result.parents[nid] = None
    result.distances[source] = 0.0

    heap: list[tuple[float, str]] = [(0.0, source)]
    finalized: set[str] = set()

    while heap:
        dist_u, u = heapq.heappop(heap)
        if u in finalized:
            continue  
        finalized.add(u)

        for (v, cost) in graph.neighbors(u):
            if v in finalized:
                continue
            new_dist = dist_u + cost
            if new_dist < result.distances[v]:
                result.distances[v] = new_dist
                result.parents[v] = u
                heapq.heappush(heap, (new_dist, v))

    return result


def shortest_path(
    graph: OrgGraph, source: str, target: str
) -> tuple[list[str] | None, float]:

    result = dijkstra(graph, source)
    path = result.path_to(target)
    return path, result.distances.get(target, math.inf)
