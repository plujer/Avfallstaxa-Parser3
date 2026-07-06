"""Models for standard tax catalog and suggestions."""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow


@dataclass
class StandardTaxRow:
    source_sheet: str
    row_number: int
    strTaxekod: str = ""
    strTaxebenamning: str = ""
    strFaktor: str = ""
    strTaxedelAvser: str = ""
    strFormel: str = ""
    curNuvarandePris: str = ""
    raw: dict[str, str] = field(default_factory=dict)


@dataclass
class StandardTaxCatalog:
    source_path: str
    rows: list[StandardTaxRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        return len(self.rows)


@dataclass
class StandardTaxSuggestion:
    parser_row: ParserTaxRow
    standard_row: StandardTaxRow | None
    status: str
    score: float
    method: str
    comment: str = ""


@dataclass
class StandardTaxSuggestionReport:
    suggestions: list[StandardTaxSuggestion] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.suggestions)

    @property
    def proposal_count(self) -> int:
        return sum(1 for item in self.suggestions if item.status == "PROPOSAL")

    @property
    def review_count(self) -> int:
        return sum(1 for item in self.suggestions if item.status == "REVIEW")

    @property
    def no_suggestion_count(self) -> int:
        return sum(1 for item in self.suggestions if item.status == "NO_SUGGESTION")
