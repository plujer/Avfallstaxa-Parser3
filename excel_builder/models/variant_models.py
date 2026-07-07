"""Variant intelligence models.

Variant intelligence explains differences inside a tax family. It is decision
support only: it does not modify Taxa_från_edp, standard tax files, or
municipality-specific project data.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaxVariantProfile:
    tax_code: str = ""
    family_code: str = ""
    volume_liter: str = ""
    waste_code: str = ""
    interval: str = ""
    variant: str = ""
    usage_type: str = ""
    source_text: str = ""
    source: str = ""

    @property
    def variant_key(self) -> str:
        parts = [
            self.volume_liter,
            self.waste_code,
            self.interval,
            self.variant,
            self.usage_type,
        ]
        value = "|".join(part for part in parts if part)
        return value or "BASE"


@dataclass(frozen=True)
class VariantComparison:
    word: TaxVariantProfile
    candidate: TaxVariantProfile
    same_family: bool
    same_variant: bool
    score: float
    matched_fields: list[str] = field(default_factory=list)
    mismatched_fields: list[str] = field(default_factory=list)
    explanation: str = ""


@dataclass
class VariantIntelligenceReport:
    profiles: list[TaxVariantProfile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_profiles(self) -> int:
        return len(self.profiles)

    @property
    def families(self) -> int:
        return len({profile.family_code for profile in self.profiles if profile.family_code})
