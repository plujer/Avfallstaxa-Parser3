"""Tax family intelligence models.

Tax families group EDP/standard tax codes by their stable base parts while
keeping intervals and variants separate. This is only decision support: it does
not modify Taxa_fran_edp or any municipality-specific source data.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.tax_code_models import ParsedTaxCode


@dataclass(frozen=True)
class TaxFamilyKey:
    prefix: str = ""
    volume_liter: str = ""
    waste_code: str = ""

    @property
    def value(self) -> str:
        return "".join(part for part in (self.prefix, self.volume_liter, self.waste_code) if part)


@dataclass
class TaxFamilyMember:
    tax_code: str
    family_key: TaxFamilyKey
    interval: str = ""
    variant: str = ""
    source: str = ""
    parsed: ParsedTaxCode | None = None

    @property
    def variant_key(self) -> str:
        return self.variant or self.interval or "BASE"


@dataclass
class TaxFamily:
    key: TaxFamilyKey
    members: list[TaxFamilyMember] = field(default_factory=list)

    @property
    def family_code(self) -> str:
        return self.key.value

    @property
    def member_count(self) -> int:
        return len(self.members)

    @property
    def intervals(self) -> list[str]:
        return sorted({member.interval for member in self.members if member.interval})

    @property
    def variants(self) -> list[str]:
        return sorted({member.variant for member in self.members if member.variant})

    def contains_code(self, tax_code: str) -> bool:
        normalized = str(tax_code or "").strip().upper().replace(" ", "").replace("-", "")
        return any(
            member.tax_code.strip().upper().replace(" ", "").replace("-", "") == normalized
            for member in self.members
        )


@dataclass
class TaxFamilyMatch:
    word_tax_code: str
    candidate_tax_code: str
    word_family: str
    candidate_family: str
    same_family: bool
    same_variant: bool = False
    explanation: str = ""


@dataclass
class TaxFamilyReport:
    families: list[TaxFamily] = field(default_factory=list)
    matches: list[TaxFamilyMatch] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total_families(self) -> int:
        return len(self.families)

    @property
    def total_members(self) -> int:
        return sum(family.member_count for family in self.families)

    def family(self, family_code: str) -> TaxFamily | None:
        normalized = str(family_code or "").strip().upper().replace(" ", "").replace("-", "")
        for family in self.families:
            if family.family_code == normalized:
                return family
        return None
