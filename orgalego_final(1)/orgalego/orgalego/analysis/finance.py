from orgalego.core.modeling.graph import OrgGraph

def payroll_by_unit(graph: OrgGraph) -> dict[str, float]:
    
    totals: dict[str, float] = {}
    
    for n in graph.nodes.values():
        if n.node_type == "person":
            totals[n.unit_axis] = totals.get(n.unit_axis, 0.0) + n.financial_flow
    return {k: round(v, 2) for k, v in totals.items()}


def payroll_by_team(graph: OrgGraph) -> dict[str, float]:
    
    out: dict[str, float] = {}
    
    for nid, n in graph.nodes.items():
        if n.node_type == "team":
            people = [v for (v, _cost) in graph.neighbors(nid) if graph.nodes[v].node_type == "person"]
            out[n.label] = round(sum(graph.nodes[p].financial_flow for p in people), 2)
    return out


def financial_flow_vs_workload(graph: OrgGraph) -> list[dict]:

    rows = []

    for nid, n in graph.nodes.items():       
        if n.node_type != "person": continue  
        load = n.workload
        ratio = round(n.financial_flow / load, 2) if load else None
        rows.append({"id": nid, "label": n.label, "role": n.role_family, "financial_flow": n.financial_flow, "workload": load, "ratio": ratio})
    return rows