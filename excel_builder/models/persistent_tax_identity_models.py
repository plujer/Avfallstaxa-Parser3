"""Models for persistent tax identities.

A persistent tax identity is a content-based identity for a Word tax point. It is
intended to remain stable when a tax row is moved to another paragraph while the
business meaning stays the same. It is not an EDP tax code and must never
replace Taxa_från_edp as facit.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from excel_builder.models.matching_models import ParserTaxRow


@dataclass
class PersistentTaxIdentity:
    persistent_tax_id: str
    content_fingerprint: str
    identity_basis: str
    occurrence: int
    parser_row: ParserTaxRow
    section_bound_word_tax_id: str
    status: str = "ACTIVE"
    comment: str = ""


@dataclass
class PersistentTaxIdentityReport:
    identities: list[PersistentTaxIdentity] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.identities)

    @property
    def duplicate_content_groups(self) -> int:
        counts: dict[str, int] = {}
        for item in self.identities:
            counts[item.content_fingerprint] = counts.get(item.content_fingerprint, 0) + 1
        return sum(1 for count in counts.values() if count > 1)

    @property
    def passed(self) -> bool:
        return not self.warnings
