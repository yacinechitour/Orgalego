from orgalego.core.modeling.graph import OrgGraph
from orgalego.algorithms.bfs import bfs
from orgalego.algorithms.dijkstra import shortest_path
from orgalego.algorithms.kosaraju import feedback_loops
from orgalego.algorithms.kruskal import kruskal
from orgalego.algorithms.betweenness import betweenness_centrality
from orgalego.analysis.finance import ( payroll_by_unit, payroll_by_team, financial_flow_vs_workload,)
from orgalego.algorithms.kosaraju import kosaraju


def _label(graph: OrgGraph, node_id: str, with_id: bool = False) -> str:

    node = graph.nodes.get(node_id)
    if node is None:
        return str(node_id)
    return f"{node_id} ({node.label})" if with_id else node.label





def run_bfs_diagnosis(graph: OrgGraph, source, target, do_print: bool = True):


    result = bfs(graph, source)
    distance = result.distances.get(target)
    path = result.path_to(target)
    if do_print:
        print(f"BFS  | source={source}  target={target}")
        print(f"  {_label(graph, source, with_id=True)}  ->  {_label(graph, target, with_id=True)}")
        if distance is None:
            print("  Unreachable.")
        else:
            readable = " -> ".join(graph.nodes[n].label for n in path)
            print(f"  Distance: {distance} hop(s)")
            print(f"  Path: {readable}")
            print(f"  Interpretation: {graph.nodes[target].label} is {distance} "
                  f"relation(s) away from {graph.nodes[source].label}.")


def run_dijkstra_diagnosis(graph: OrgGraph, source, target, do_print: bool = True):


    comm = graph.as_merged_undirected()
    path, cost = shortest_path(comm, source, target)
    if do_print:
        print(f"Dijkstra  | source={source}  target={target}")
        if path is None:
            print("  No path.")
        else:
            print(f"  Total cost: {round(cost, 2)}")
            print("  Path:")
            for nid in path:
                n = graph.nodes[nid]
                print(f"    {nid} -> {n.label} ({n.role_family})")
            if len(path) > 2:
                relays = ", ".join(graph.nodes[n].label for n in path[1:-1])
                print(f"  Interpretation: communication must go through {relays}.")


def run_kosaraju_diagnosis(graph: OrgGraph, do_print: bool = True):


    components = kosaraju(graph)
    loops = [c for c in components if len(c) > 1]
    if do_print:
        print(f"Kosaraju  | {len(components)} components, {len(loops)} loop(s)")
        for comp in loops:
            print("  Loop:", [graph.nodes[n].label for n in comp])
        if loops:
            print("  Interpretation: inside each loop, members depend on one "
                  "another mutually (e.g. a cohort: representative <-> contributors).")
        else:
            print("  No dependency loop: the directed graph is acyclic.")


def run_kruskal_diagnosis(
    graph: OrgGraph,
    do_print: bool = True,
    root_id: str | None = None,
    max_depth: int = 9,
    max_children: int = 12,
):


    comm = graph.as_merged_undirected()
    mst = kruskal(comm)
    total = mst.total_weight()

    original_edges = len(comm.edges)
    kept_edges = len(mst.edges)
    removed_edges = original_edges - kept_edges

    if do_print:
        print(
            f"Kruskal | original edges: {original_edges} | "
            f"kept edges: {kept_edges} | "
            f"removed edges: {removed_edges} | "
            f"total weight: {total}"
        )

        if root_id is None:
            root_id = max(
                mst.nodes.keys(),
                key=lambda nid: graph.nodes[nid].rank
            )

        print(f"\nMST tree rooted at: {graph.nodes[root_id].label}\n")

        visited = set()

        def print_tree(node_id: str, prefix: str = "", depth: int = 0) -> None:
            visited.add(node_id)
            node = graph.nodes[node_id]

            if depth == 0:
                print(node.label)

            if depth >= max_depth:
                return

            children = [
                (v, weight)
                for v, weight in mst.neighbors(node_id)
                if v not in visited
            ]

            children.sort(
                key=lambda x: (
                    -graph.nodes[x[0]].rank,
                    graph.nodes[x[0]].label
                )
            )

            shown_children = children[:max_children]

            for i, (child_id, weight) in enumerate(shown_children):
                is_last = i == len(shown_children) - 1 and len(children) <= max_children

                connector = "└── " if is_last else "├── "
                next_prefix = prefix + ("    " if is_last else "│   ")

                child = graph.nodes[child_id]

                print(
                    f"{prefix}{connector}{child.label} "
                    f"(weight={round(weight, 3)}, rank={child.rank})"
                )

                print_tree(child_id, next_prefix, depth + 1)

            if len(children) > max_children:
                print(
                    f"{prefix}└── ... (+{len(children) - max_children} more)"
                )

        print_tree(root_id)



def run_betweenness_diagnosis(graph: OrgGraph, top_k: int = 10, do_print: bool = True):


    scores = betweenness_centrality(graph.as_merged_undirected())
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    if do_print:
        print(f"Betweenness  | top {top_k} most central")
        print(f"  {'ID':>3} | {'Label':24} | {'Role / type':24} | score")
        print("  " + "-" * 64)
        for nid, score in ranked[:top_k]:
            n = graph.nodes[nid]
            kind = n.role_family or n.node_type
            print(f"  {nid:>3} | {n.label:24.24} | {kind:24.24} | {score}")
        print("  Interpretation: high score = frequent transit point, hence a "
              "potential bottleneck if unavailable.")


def run_louvain_diagnosis(graph: OrgGraph, band=None, do_print: bool = True):


    from orgalego.algorithms.louvain import detect_silos

    result = detect_silos(graph.as_merged_undirected(), band=band)
    if do_print:
        print("Louvain  | community detection (NetworkX)")
        print(f"  Modularity: {result['modularity']}")
        print(f"  {len(result['communities'])} communities:")
        for i, comm in enumerate(result["communities"], 1):
            labels = [graph.nodes[n].label for n in comm if n in graph.nodes]
            print(f"    Community {i} ({len(labels)}): {labels}")
        print("  Interpretation: high modularity = tightly-knit groups loosely "
              "linked to each other (silos).")


def run_finance_report(graph: OrgGraph, do_print: bool = True):

    by_unit = payroll_by_unit(graph)
    by_team = payroll_by_team(graph)
    ratios = financial_flow_vs_workload(graph)
    total = round(sum(n.financial_flow for n in graph.nodes.values()), 2)
    income = round(sum(n.financial_flow for n in graph.nodes.values() if n.financial_flow > 0), 2)
    cost = round(sum(n.financial_flow for n in graph.nodes.values() if n.financial_flow < 0), 2)

    if do_print:
        print("MONEY FLOW  | sign: negative = paid out, positive = income")
        print("=" * 60)
        print(f"  Income (positive flows): {income:>12,.0f}")
        print(f"  Cost (negative flows):  {cost:>12,.0f}")
        print(f"  NET balance:            {total:>12,.0f}")
        print()
        print("  Net balance per unit:")
        for k, v in sorted(by_unit.items(), key=lambda kv: kv[1]):
            print(f"    {k:24} {v:>12,.0f}")
        print()
        print("  Net balance per team:")
        for k, v in sorted(by_team.items(), key=lambda kv: kv[1]):
            print(f"    {k:40.40} {v:>12,.0f}")
        print()

        paid = [r for r in ratios if r["ratio"] is not None and r["financial_flow"] < 0]
        print("  Most expensive per unit of work (financial_flow / workload):")
        for r in sorted(paid, key=lambda r: r["ratio"])[:5]:
            print(f"    {r['label']:28.28} flow={r['financial_flow']:>7,.0f} "
                  f"load={r['workload']:>5} ratio={r['ratio']:>9,.0f}")
