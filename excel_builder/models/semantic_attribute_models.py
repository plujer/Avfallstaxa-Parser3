"""Semantic attribute intelligence models.

Semantic attributes are conservative decision-support signals extracted from tax
names and supporting text. They never override Taxa_från_edp and never modify
municipality-specific data.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SemanticAttributeProfile:
    tax_code: str = ""
    source_text: str = ""
    source: str = ""
    materials: tuple[str, ...] = ()
    waste_types: tuple[str, ...] = ()
    units: tuple[str, ...] = ()
    container_types: tuple[str, ...] = ()
    intervals: tuple[str, ...] = ()
    property_types: tuple[str, ...] = ()

    @property
    def attribute_key(self) -> str:
        parts = [
            ",".join(self.materials),
            ",".join(self.waste_types),
            ",".join(self.units),
            ",".join(self.container_types),
            ",".join(self.intervals),
            ",".join(self.property_types),
        ]
        value = "|".join(part for part in parts if part)
        return value or "NO_ATTRIBUTES"

    @property
    def attribute_count(self) -> int:
        return sum(
            len(values)
            for values in [
                self.materials,
                self.waste_types,
                self.units,
                self.container_types,
                self.intervals,
                self.property_types,
            ]
        )


@dataclass(frozen=True)
class SemanticAttributeComparison:
    word: SemanticAttributeProfile
    candidate: SemanticAttributeProfile
    score: float
    matched_attributes: list[str] = field(default_factory=list)
    missing_attributes: list[str] = field(default_factory=list)
    explanation: str = ""


@dataclass
class SemanticAttributeReport:
    profiles: list[SemanticAttributeProfile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_profiles(self) -> int:
        return len(self.profiles)

    @property
    def profiles_with_attributes(self) -> int:
        return sum(1 for profile in self.profiles if profile.attribute_count > 0)
