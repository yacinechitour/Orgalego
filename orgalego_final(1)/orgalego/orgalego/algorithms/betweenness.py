from orgalego.core.modeling.graph import OrgGraph


def betweenness_centrality(
    graph: OrgGraph,
    normalized: bool = True,
    weighted: bool = True,
) -> dict[str, float]:

    import networkx as nx
    from orgalego.core.modeling.graph import merged_pairs

    # Build a NetworkX graph that preserves our orientation.
    directed = any(e.directed for e in graph.edges)
    if directed:
        nxg = nx.DiGraph()
        for nid in graph.node_ids():
            nxg.add_node(nid)
        # In a directed graph A -> B and B -> A are distinct edges, each
        # keeping its own weight.
        for e in graph.edges:
            if nxg.has_edge(e.source, e.target):
                nxg[e.source][e.target]["weight"] += e.weight
            else:
                nxg.add_edge(e.source, e.target, weight=e.weight)
            if not e.directed:
                # an undirected relation inside a DiGraph needs the reverse too
                if nxg.has_edge(e.target, e.source):
                    nxg[e.target][e.source]["weight"] += e.weight
                else:
                    nxg.add_edge(e.target, e.source, weight=e.weight)
    else:
        # Undirected: the two opposite flows collapse onto one edge whose
        # weight is their SUM (consistent with Kruskal / Louvain), via the
        # shared merge helper.
        nxg = nx.Graph()
        for nid in graph.node_ids():
            nxg.add_node(nid)
        for (u, v), w in merged_pairs(graph).items():
            nxg.add_edge(u, v, weight=w)

    weight_attr = "weight" if weighted else None
    scores = nx.betweenness_centrality(
        nxg, normalized=normalized, weight=weight_attr
    )
    return {nid: round(score, 4) for nid, score in scores.items()}
