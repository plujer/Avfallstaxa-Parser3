"""Models for Excel Builder matching."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkbookTaxRow:
    row_number: int
    section: str
    paragraph_name: str
    tax_point: str
    variant: str
    unit: str
    tax_code: str
    proposed_price: str
    source_sheet: str = "Taxepunkter"


@dataclass
class ParserTaxRow:
    section: str
    tax_point: str
    variant: str = ""
    unit: str = ""
    price: str = ""


@dataclass
class MatchCandidate:
    parser_row: ParserTaxRow
    workbook_row: WorkbookTaxRow | None
    status: str
    method: str
    score: float
    comment: str = ""


@dataclass
class MatchReport:
    candidates: list[MatchCandidate] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.candidates)

    @property
    def exact(self) -> int:
        return sum(1 for item in self.candidates if item.status == "EXACT")

    @property
    def probable(self) -> int:
        return sum(1 for item in self.candidates if item.status == "PROBABLE")

    @property
    def new(self) -> int:
        return sum(1 for item in self.candidates if item.status == "NEW")

    @property
    def review(self) -> int:
        return sum(1 for item in self.candidates if item.status == "REVIEW")
