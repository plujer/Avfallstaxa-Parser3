"""Workbook profile models for Arbets-Excel analysis."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ColumnProfile:
    index: int
    letter: str
    header: str = ""
    hidden: bool = False
    width: float | None = None
    non_empty_count: int = 0
    formula_count: int = 0


@dataclass
class TableProfile:
    name: str
    ref: str
    columns: list[str] = field(default_factory=list)


@dataclass
class DataValidationProfile:
    type: str
    sqref: str
    formula1: str = ""
    formula2: str = ""


@dataclass
class SheetProfile:
    name: str
    max_row: int
    max_column: int
    hidden_state: str = "visible"
    frozen_panes: str = ""
    merged_ranges: list[str] = field(default_factory=list)
    tables: list[TableProfile] = field(default_factory=list)
    columns: list[ColumnProfile] = field(default_factory=list)
    data_validations: list[DataValidationProfile] = field(default_factory=list)
    likely_header_row: int | None = None
    detected_fields: dict[str, str] = field(default_factory=dict)


@dataclass
class WorkbookProfile:
    path: str
    sheets: list[SheetProfile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def sheet_count(self) -> int:
        return len(self.sheets)
