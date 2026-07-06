"""Models for Excel Builder."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BuilderInputRow:
    section: str
    name: str
    variant: str = ""
    unit: str = ""
    price: str = ""
    group: str = ""
    source: str = "parser"


@dataclass
class BuilderResult:
    rows: list[BuilderInputRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        return len(self.rows)
