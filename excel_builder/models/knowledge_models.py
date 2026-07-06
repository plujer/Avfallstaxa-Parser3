"""Tax knowledge models.

The Tax Knowledge layer extracts structured meaning from Word/parser rows before
we try to match against EDP or standard taxes.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow


@dataclass
class TaxKnowledgeFeature:
    parser_row: ParserTaxRow
    section_group: str = ""
    category: str = ""
    waste_type: str = ""
    unit_type: str = ""
    container_volume_liter: str = ""
    factor_hint: str = ""
    keywords: list[str] = field(default_factory=list)
    confidence: float = 0.0
    notes: list[str] = field(default_factory=list)


@dataclass
class TaxKnowledgeReport:
    features: list[TaxKnowledgeFeature] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.features)

    def count_category(self, category: str) -> int:
        return sum(1 for item in self.features if item.category == category)

    def count_factor_hint(self, factor_hint: str) -> int:
        return sum(1 for item in self.features if item.factor_hint == factor_hint)
