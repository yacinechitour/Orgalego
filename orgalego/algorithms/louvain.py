
from orgalego.core.modeling.graph import OrgGraph


def _induced_band_subgraph(graph: OrgGraph, band: str) -> OrgGraph:

    sub = OrgGraph()
    keep = set(graph.get_band_nodes(band))
    for nid in keep:
        sub.add_node(graph.nodes[nid])
    for edge in graph.edges:
        if edge.source in keep and edge.target in keep:
            sub.add_edge(edge)
    return sub


def detect_silos(graph: OrgGraph, band: str | None = None) -> dict:

    import networkx as nx
    from networkx.algorithms.community import louvain_communities, modularity

    target = _induced_band_subgraph(graph, band) if band is not None else graph

    # Build an undirected weighted NetworkX graph from ours. The two opposite
    # flows A -> B and B -> A are merged into a single undirected edge whose
    # weight is their SUM (the total work exchanged), so the modularity sees
    # the real strength of the link instead of a single arbitrary direction.
    from orgalego.core.modeling.graph import merged_pairs
    nxg = nx.Graph()
    for nid in target.node_ids():
        nxg.add_node(nid)
    for (u, v), weight in merged_pairs(target).items():
        nxg.add_edge(u, v, weight=weight)

    if nxg.number_of_edges() == 0:
        return {"communities": [], "modularity": 0.0}

    communities = louvain_communities(nxg, weight="weight", seed=42)
    mod = modularity(nxg, communities, weight="weight")

    return {
        "communities": [sorted(c) for c in communities],
        "modularity": round(mod, 4),
    }
