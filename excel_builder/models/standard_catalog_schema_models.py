"""Schema models for standard tax catalog reverse engineering."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class StandardCatalogSection:
    sheet_name: str
    header_row: int
    start_row: int
    end_row: int
    headers: list[str] = field(default_factory=list)
    row_count: int = 0
    key_columns: list[str] = field(default_factory=list)


@dataclass
class StandardCatalogSheetSchema:
    name: str
    max_row: int
    max_column: int
    sections: list[StandardCatalogSection] = field(default_factory=list)
    tables: list[str] = field(default_factory=list)
    merged_ranges: list[str] = field(default_factory=list)
    formula_count: int = 0
    warnings: list[str] = field(default_factory=list)


@dataclass
class StandardCatalogSchema:
    source_path: str
    sheets: list[StandardCatalogSheetSchema] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def sheet_count(self) -> int:
        return len(self.sheets)

    @property
    def section_count(self) -> int:
        return sum(len(sheet.sections) for sheet in self.sheets)

    @property
    def estimated_standard_rows(self) -> int:
        return sum(section.row_count for sheet in self.sheets for section in sheet.sections)
