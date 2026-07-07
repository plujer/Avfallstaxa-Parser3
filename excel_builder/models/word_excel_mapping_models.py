"""Models for deterministic Word to Excel tax mapping."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow, WorkbookTaxRow


@dataclass
class WordExcelMappingItem:
    word_tax_id: str
    stable_tax_identity: str
    content_fingerprint: str
    parser_row: ParserTaxRow
    workbook_row: WorkbookTaxRow | None
    status: str
    method: str
    confidence: float
    comment: str = ""
    duplicate_edp_allowed: bool = True


@dataclass
class WordExcelMappingReport:
    items: list[WordExcelMappingItem] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def mapped(self) -> int:
        return sum(1 for item in self.items if item.status == "MAPPED")

    @property
    def review(self) -> int:
        return sum(1 for item in self.items if item.status == "REVIEW")

    @property
    def missing(self) -> int:
        return sum(1 for item in self.items if item.status == "MISSING")

    @property
    def passed(self) -> bool:
        return self.missing == 0
