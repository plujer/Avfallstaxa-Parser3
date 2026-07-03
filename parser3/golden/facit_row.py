"""Golden master row model."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class FacitRow:
    section: str
    name: str
    variant: str = ""
    unit: str = ""
    group: str = ""
    ewc: str = ""
    un_number: str = ""
    export: bool = True
    comment: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
