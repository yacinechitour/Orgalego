# OrgaLego

**Modeling an Organization as a Weighted Directed Graph and Diagnosing It with Graph Algorithms.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![NetworkX](https://img.shields.io/badge/Dependency-NetworkX-lightgrey.svg)](https://networkx.org/)
[![PSL](https://img.shields.io/badge/Universit%C3%A9%20PSL-IBSAI-1a5276.svg)]()

---

## Overview

Traditional organizational charts are descriptive but computationally inert—they hide systemic bottlenecks, shadow teams, and approval deadlocks.

**OrgaLego** operationalizes any corporate or academic structure by mapping its entities, roles, and interactions onto a single **weighted, directed graph** $G = (V, E)$. Running a suite of graph algorithms turns high-level managerial inquiries into deterministic mathematical diagnostics.

---

## Core Modeling Philosophy

OrgaLego models any organization from two minimal primitives:

- **Nodes ($v \in V$):** Discrete entities (parent organization, schools/divisions, research labs, support departments, or individual personnel). Each node carries a normalized hierarchical **rank** $\in [0, 10]$, partitioned into three operational bands:
  - **Base:** $[0, 4)$
  - **Intermediate:** $[4, 7)$
  - **Top:** $[7, 10]$
- **Edges ($e \in E$):** Directional workflow or communication pipelines with weight $w(u, v)$ representing real-world coordination cost or interaction intensity. Reciprocal yet asymmetric relationships are represented as pairs of anti-parallel directed edges.

Complex metrics are derived dynamically from the topology rather than hardcoded—for example, an individual's operational **workload**:

$$\text{Workload}(v) = \sum_{(u \to v) \in E} w(u, v)$$

---

## The Six-Lens Algorithmic Framework

Core traversal, shortest-path, connectivity, and spanning-tree algorithms (**BFS, Dijkstra, Kosaraju, Kruskal**) were implemented **entirely from scratch** using Python's standard library, while advanced topological community detection leverages optimized wrappers.

| Managerial Lens | Graph Algorithm | Implementation | Operational Diagnostic & Application |
| :--- | :--- | :---: | :--- |
| **Hierarchical Depth** | Breadth-First Search (`bfs.py`) | From scratch | Shortest unweighted path from any member to the executive node to measure vertical distance. |
| **Coordination Cost** | Dijkstra (`dijkstra.py`) | From scratch | Fastest communication channels between units, treating edge weights as coordination friction. |
| **Dependency Loops** | Kosaraju SCC (`kosaraju.py`) | From scratch | Detects Strongly Connected Components where circular approvals create validation deadlocks. |
| **Coordination Backbone** | Kruskal MST + Union-Find (`kruskal.py`) | From scratch | Extracts the minimum-cost spanning backbone to safeguard essential paths during restructuring. |
| **Key-Person Risk** | Betweenness Centrality (`betweenness.py`) | Custom / Graph Core | Flags structural bottlenecks by measuring how often a node sits on optimal communication paths. |
| **Silo Detection** | Louvain Community Detection (`louvain_wrapper.py`) | Wrapper (`networkx`) | Partitions the graph by actual interaction density to expose organizational silos and shadow teams. |

### Additional Analysis Modules
- **`diagnosis.py`:** Formats raw algorithmic outputs into executive-ready diagnostic reports consumed by `demo.ipynb`.
- **`sensitivity.py`:** Restructuring simulation engine to evaluate topological impact before organizational changes.
- **`finance.py`:** Models signed budgetary and monetary flows across units.

---

## Production Validation: Synthesized Université PSL Ecosystem

To stress-test scalability and real-world interpretability, OrgaLego was validated on a comprehensive fictionalized structural dataset of **Université PSL** stored as a single source of truth in `data/org_master.json`:

- **Scale:** **623 nodes** and **1,512 directed weighted edges**.
- **Institutional Entities:** 1 master university node, 8 specialized schools (e.g., Mines Paris, ESPCI, ENS), 35 academic departments & research labs, and 19 cross-functional support units (administrative boards, sports associations, student unions, housing committees).
- **Personnel Population:** 560 simulated members (244 undergraduate/graduate students, 90 PhD candidates, 61 full-time researchers, 56 faculty instructors, 19 administrative leads, and 16 laboratory directors).
- **Cross-Affiliations:** **65 multi-affiliated personnel** (e.g., joint teaching/research appointments across schools or committee seats), providing a realistic stress test for Betweenness bottlenecks and Louvain silo detection.
- **Interactive Macro Visualization (`psl_organisation.html`):** A standalone interactive HTML network graph allowing browser-based exploration of clusters, Louvain communities, and cross-institutional touchpoints.

---

## Repository Structure

```text
orgalego/
├── demo.ipynb               # Interactive Analysis & Demonstration Notebook
├── requirements.txt         # Minimal external dependencies (networkx)
├── psl_organisation.html    # Interactive Macro Graph Visualization (PSL)
├── data/
│   └── org_master.json      # Single Source of Truth (JSON schema)
└── orgalego/
    ├── __init__.py
    ├── core/
    │   ├── modeling/        # Core primitives (node.py, edge.py, graph.py)
    │   └── loader.py        # Validating JSON parser & graph builder
    ├── algorithms/
    │   ├── bfs.py           # Breadth-First Search (Hierarchical Depth)
    │   ├── dijkstra.py      # Shortest Path (Communication Efficiency)
    │   ├── kosaraju.py      # Strongly Connected Components (Dependency Loops)
    │   ├── kruskal.py       # Minimum Spanning Tree via Union-Find (Backbone)
    │   ├── betweenness.py   # Centrality Mapping (Key-Person Risk)
    │   └── louvain_wrapper.py # Community Detection (Silo Resolution)
    └── analysis/
        ├── diagnosis.py     # Polished Reporting & Visualization Wrappers
        ├── sensitivity.py   # Restructuring Simulation Engine
        └── finance.py       # Signed Budgetary & Monetary Flows
```



To inspect the full macro-scale graph directly in your browser, open `psl_organisation.html`.

---

## Authors

- **Yacine Chitour**
- **Rayane**

*Inaugural Cohort, International Bachelor of Science in Artificial Intelligence (IBSAI / PSAI) — Université PSL (June 2026)*
