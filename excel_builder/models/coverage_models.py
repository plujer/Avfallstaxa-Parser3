"""Coverage models for Word tax rows in Taxepunkter."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow, WorkbookTaxRow


@dataclass
class CoverageItem:
    parser_row: ParserTaxRow
    workbook_row: WorkbookTaxRow | None
    status: str
    method: str
    comment: str = ""


@dataclass
class CoverageReport:
    items: list[CoverageItem] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def covered(self) -> int:
        return sum(1 for item in self.items if item.status == "COVERED")

    @property
    def missing(self) -> int:
        return sum(1 for item in self.items if item.status == "MISSING")

    @property
    def review(self) -> int:
        return sum(1 for item in self.items if item.status == "REVIEW")

    @property
    def passed(self) -> bool:
        return self.missing == 0
