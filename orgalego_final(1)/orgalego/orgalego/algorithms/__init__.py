"""Hand-coded graph algorithms and small helpers shared between them."""


def reconstruct_path(parents: dict[str, str | None], target: str) -> list[str]:
    """Rebuild a path by walking the ``parents`` chain back from ``target``.

    Shared by BFS and Dijkstra, whose only difference is the reachability
    guard (handled by each caller before delegating here).
    """
    path: list[str] = []
    current: str | None = target
    while current is not None:
        path.append(current)
        current = parents.get(current)
    path.reverse()
    return path
