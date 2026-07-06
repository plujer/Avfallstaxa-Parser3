from dataclasses import dataclass, field

@dataclass
class SemanticRow:
    row_type: str
    text: str
    cells: list[str] = field(default_factory=list)
    order: int = 0
    section: str = ""
    group: str = ""
    reason: str = ""
