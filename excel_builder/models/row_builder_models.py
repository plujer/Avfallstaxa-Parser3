"""Models for building the complete Taxepunkter row plan."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models import ParserTaxRow, WorkbookTaxRow


@dataclass
class TaxepunkterBuildRow:
    parser_row: ParserTaxRow
    workbook_row: WorkbookTaxRow | None
    action: str
    method: str
    comment: str = ""

    @property
    def excel_row_number(self) -> int | None:
        return self.workbook_row.row_number if self.workbook_row else None


@dataclass
class TaxepunkterBuildPlan:
    rows: list[TaxepunkterBuildRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_parser_rows(self) -> int:
        return len(self.rows)

    @property
    def reuse_count(self) -> int:
        return sum(1 for row in self.rows if row.action == "REUSE")

    @property
    def create_count(self) -> int:
        return sum(1 for row in self.rows if row.action == "CREATE")

    @property
    def review_count(self) -> int:
        return sum(1 for row in self.rows if row.action == "REVIEW")

    @property
    def passed_coverage(self) -> bool:
        # A valid plan always has exactly one plan row per parser row.
        return self.total_parser_rows > 0 and all(row.action in {"REUSE", "CREATE", "REVIEW"} for row in self.rows)
