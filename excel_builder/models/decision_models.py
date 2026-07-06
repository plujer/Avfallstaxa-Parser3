"""Decision models for one consolidated Taxepunkter decision per Word tax."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow, WorkbookTaxRow
from excel_builder.models.standard_tax_models import StandardTaxRow


@dataclass
class TaxDecision:
    parser_row: ParserTaxRow
    status: str
    source: str
    rule: str
    confidence: float
    workbook_row: WorkbookTaxRow | None = None
    standard_row: StandardTaxRow | None = None
    comment: str = ""


@dataclass
class TaxDecisionReport:
    decisions: list[TaxDecision] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.decisions)

    def count_status(self, status: str) -> int:
        return sum(1 for item in self.decisions if item.status == status)

    @property
    def edp_match(self) -> int:
        return self.count_status("EDP_MATCH")

    @property
    def standard_proposal(self) -> int:
        return self.count_status("STANDARD_PROPOSAL")

    @property
    def review_required(self) -> int:
        return self.count_status("REVIEW_REQUIRED")

    @property
    def new_taxa(self) -> int:
        return self.count_status("NEW_TAXA")
