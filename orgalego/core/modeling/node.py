from dataclasses import dataclass

@dataclass
class Node:

    id: str
    label: str
    rank: float
    node_type: str = "entity"
    workload: float = 0.0
    group_key: str | None = None
    unit_axis: str = ""
    financial_flow: float = 0.0
    attributes: dict | None = None
    role_family: str = ""
    role_title: str = ""

    def __post_init__(self) -> None:
        if self.attributes is None:
            self.attributes = {}
        if not (0 <= self.rank <= 10):
            raise ValueError(
                f"Invalid rank for node '{self.id}': {self.rank}. "
                f"rank must be between 0 (base) and 10 (top)."
            )

    
    @property
    def band(self) -> str:

        if 0 <= self.rank < 4:
            return "base"
        if 4 <= self.rank < 7:
            return "intermediate"
        if 7 <= self.rank <= 10:
            return "top"
        raise ValueError(f"rank must be between 0 and 10 (got {self.rank}).")

