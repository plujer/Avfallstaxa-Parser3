"""Context models for enriching parser tax rows.

The context resolver improves Word understanding by allowing rows to inherit
meaning from nearby headings, section names, parent rows and repeated words.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow


@dataclass
class ParserTaxContext:
    row_index: int
    parser_row: ParserTaxRow
    section_context: str = ""
    property_type_context: str = ""
    waste_type_context: str = ""
    container_context: str = ""
    service_context: str = ""
    inherited_text: str = ""
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)


@dataclass
class ContextResolvedTaxRow:
    original_row: ParserTaxRow
    enriched_row: ParserTaxRow
    context: ParserTaxContext


@dataclass
class ContextResolutionReport:
    rows: list[ContextResolvedTaxRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.rows)

    @property
    def enriched_count(self) -> int:
        return sum(1 for row in self.rows if row.enriched_row != row.original_row)
