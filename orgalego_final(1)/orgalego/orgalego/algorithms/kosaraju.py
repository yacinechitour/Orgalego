from orgalego.core.modeling.graph import OrgGraph


def _build_directed_adjacency(graph: OrgGraph) -> dict[str, list[str]]:

    adj: dict[str, list[str]] = {nid: [] for nid in graph.node_ids()}
    for u in graph.node_ids():
        for (v, _c) in graph.neighbors(u):
            adj[u].append(v)
    return adj


def _transpose(adj: dict[str, list[str]]) -> dict[str, list[str]]:
    """Return the transposed adjacency (every arrow reversed)."""
    transposed: dict[str, list[str]] = {u: [] for u in adj}
    for u in adj:
        for v in adj[u]:
            transposed[v].append(u)
    return transposed


def _dfs_finish_order(adj: dict[str, list[str]]) -> list[str]:

    visited: set[str] = set()
    order: list[str] = []

    for start in adj:
        if start in visited:
            continue
        stack: list[tuple[str, bool]] = [(start, False)]
        while stack:
            node, processed = stack.pop()
            if processed:
                order.append(node)  
                continue
            if node in visited:
                continue
            visited.add(node)
            stack.append((node, True))  
            for nb in adj[node]:
                if nb not in visited:
                    stack.append((nb, False))

    return order


def _dfs_collect(adj: dict[str, list[str]], start: str, visited: set[str]) -> list[str]:
    component: list[str] = []
    stack: list[str] = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        component.append(node)
        for nb in adj[node]:
            if nb not in visited:
                stack.append(nb)
    return component


def kosaraju(graph: OrgGraph) -> list[list[str]]:
    """Return the list of strongly connected components of the graph.

    Each component is a list of node identifiers.
    """
    adj = _build_directed_adjacency(graph)

    finish_order = _dfs_finish_order(adj)

    transposed = _transpose(adj)

    visited: set[str] = set()
    components: list[list[str]] = []
    for node in reversed(finish_order):
        if node not in visited:
            comp = _dfs_collect(transposed, node, visited)
            components.append(comp)

    return components


def feedback_loops(graph: OrgGraph) -> list[list[str]]:
    return [comp for comp in kosaraju(graph) if len(comp) > 1]
