"""Semantic profile models for tax matching.

A semantic profile is a common normalized representation for taxes from Word,
EDP, standard tax catalog, and the master rule repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaxSemanticProfileKey:
    category: str = ""
    waste_type: str = ""
    service_type: str = ""
    container_type: str = ""
    container_volume_liter: str = ""
    interval: str = ""
    property_type: str = ""
    unit_type: str = ""
    factor_hint: str = ""


@dataclass
class TaxSemanticProfile:
    source: str
    source_id: str
    key: TaxSemanticProfileKey
    source_text: str = ""
    tax_code: str = ""
    standard_tax_code: str = ""
    confidence: float = 0.0
    keywords: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class TaxSemanticProfileReport:
    profiles: list[TaxSemanticProfile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.profiles)

    def by_source(self, source: str) -> list[TaxSemanticProfile]:
        return [profile for profile in self.profiles if profile.source == source]
