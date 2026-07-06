from dataclasses import dataclass

@dataclass
class DiffItem:
    status: str
    section: str
    name: str
    variant: str = ""
    unit: str = ""
    reason: str = ""
