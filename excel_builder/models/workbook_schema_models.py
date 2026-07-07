"""Workbook schema models for master workbook reverse engineering."""

from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class HeaderCandidate:
    row_number: int
    non_empty_count: int
    score: float
    values: list[str] = field(default_factory=list)

@dataclass
class SheetSchema:
    name: str
    max_row: int
    max_column: int
    visible_state: str = "visible"
    freeze_panes: str = ""
    tables: list[str] = field(default_factory=list)
    merged_ranges: list[str] = field(default_factory=list)
    data_validations: int = 0
    auto_filter_ref: str = ""
    header_candidates: list[HeaderCandidate] = field(default_factory=list)
    detected_header_row: int | None = None
    detected_headers: list[str] = field(default_factory=list)
    formula_count: int = 0
    hidden_columns: list[str] = field(default_factory=list)
    hidden_rows: list[int] = field(default_factory=list)

@dataclass
class WorkbookSchema:
    workbook_path: str
    sheets: list[SheetSchema] = field(default_factory=list)
    defined_names: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def sheet_count(self) -> int:
        return len(self.sheets)

    def sheet(self, name: str) -> SheetSchema | None:
        for sheet in self.sheets:
            if sheet.name == name:
                return sheet
        return None
