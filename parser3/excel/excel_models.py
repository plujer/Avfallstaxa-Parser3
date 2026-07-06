"""Excel/facit models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SheetProfile:
    sheet_name: str
    max_row: int
    max_column: int
    header_row: int | None = None
    headers: list[str] = field(default_factory=list)
    detected_columns: dict[str, int] = field(default_factory=dict)
    candidate_score: int = 0


@dataclass
class WorkbookProfile:
    path: str
    sheets: list[SheetProfile] = field(default_factory=list)

    @property
    def best_sheet(self) -> SheetProfile | None:
        if not self.sheets:
            return None
        return sorted(self.sheets, key=lambda s: s.candidate_score, reverse=True)[0]
