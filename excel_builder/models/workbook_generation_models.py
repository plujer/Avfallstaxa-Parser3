"""Models for final workbook generation and decision trace writing."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WorkbookDecisionRow:
    """Decision trace row prepared for workbook output."""

    word_tax_code: str
    candidate_tax_code: str
    decision: str
    confidence: float
    total_score: float
    primary_reason: str
    rejected_reason: str = ""
    signals: str = ""


@dataclass
class WorkbookGenerationReport:
    """Summary from writing decision support into a workbook."""

    workbook_path: str
    rows_written: int = 0
    taxepunkter_rows_updated: int = 0
    warnings: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "OK" if not self.warnings else "WARNING"
