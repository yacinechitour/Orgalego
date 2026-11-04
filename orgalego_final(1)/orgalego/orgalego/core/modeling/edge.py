from dataclasses import dataclass


@dataclass
class Edge:

    source: str
    target: str
    weight: float = 1.0
    directed: bool = False

    def __post_init__(self) -> None:
        if self.source == self.target:
            raise ValueError(
                f"Invalid edge: self-loop on '{self.source}' is not allowed."
            )
        if self.weight < 0:
            raise ValueError(
                f"Negative weight not allowed on edge "
                f"{self.source} -> {self.target}: {self.weight}."
            )
