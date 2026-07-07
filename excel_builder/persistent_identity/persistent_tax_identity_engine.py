"""Persistent identity engine for Word tax rows.

The engine creates two IDs:
- ``section_bound_word_tax_id``: exact trace ID for the current Word structure.
- ``persistent_tax_id``: content-based ID intended to survive paragraph moves.

Repeated rows with identical content are allowed. They receive the same base
fingerprint and an occurrence suffix so each physical Word row remains uniquely
traceable. This is a QA signal, not an automatic error.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict

from excel_builder.matching import MatchNormalizer
from excel_builder.models import ParserTaxRow
from excel_builder.models.persistent_tax_identity_models import (
    PersistentTaxIdentity,
    PersistentTaxIdentityReport,
)


class PersistentTaxIdentityEngine:
    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def build(self, parser_rows: list[ParserTaxRow]) -> PersistentTaxIdentityReport:
        report = PersistentTaxIdentityReport()
        occurrence_by_basis: dict[str, int] = defaultdict(int)
        occurrence_by_section_basis: dict[str, int] = defaultdict(int)

        for row in parser_rows:
            basis = self.identity_basis(row)
            occurrence_by_basis[basis] += 1
            occurrence = occurrence_by_basis[basis]

            section_basis = self.section_bound_basis(row)
            occurrence_by_section_basis[section_basis] += 1

            fingerprint = self.content_fingerprint(row)
            persistent_id = self.persistent_tax_id(row, occurrence)
            section_id = self.section_bound_word_tax_id(row, occurrence_by_section_basis[section_basis])
            comment = "Persistent ID baseras på taxepunkt, variant och enhet, inte paragraf."
            if occurrence > 1:
                comment += " Samma innehåll förekommer flera gånger; det är granskningsinformation, inte automatiskt fel."

            report.identities.append(
                PersistentTaxIdentity(
                    persistent_tax_id=persistent_id,
                    content_fingerprint=fingerprint,
                    identity_basis=basis,
                    occurrence=occurrence,
                    parser_row=row,
                    section_bound_word_tax_id=section_id,
                    comment=comment,
                )
            )

        self._add_duplicate_notes(report)
        return report

    def identity_basis(self, row: ParserTaxRow) -> str:
        return self.normalizer.row_key("", row.tax_point, row.variant, row.unit)

    def section_bound_basis(self, row: ParserTaxRow) -> str:
        return self.normalizer.row_key(row.section, row.tax_point, row.variant, row.unit)

    def content_fingerprint(self, row: ParserTaxRow) -> str:
        return hashlib.sha1(self.identity_basis(row).encode("utf-8")).hexdigest().upper()

    def persistent_tax_id(self, row: ParserTaxRow, occurrence: int = 1) -> str:
        digest = self.content_fingerprint(row)[:12]
        return f"PTX-{digest}-{occurrence:02d}"

    def section_bound_word_tax_id(self, row: ParserTaxRow, occurrence: int = 1) -> str:
        digest = hashlib.sha1(self.section_bound_basis(row).encode("utf-8")).hexdigest()[:8].upper()
        section = re.sub(r"[^0-9A-Za-z]+", "-", row.section).strip("-") or "NOSECTION"
        return f"WTX-{section}-{digest}-{occurrence:02d}"

    def _add_duplicate_notes(self, report: PersistentTaxIdentityReport) -> None:
        by_fingerprint: dict[str, list[PersistentTaxIdentity]] = defaultdict(list)
        for item in report.identities:
            by_fingerprint[item.content_fingerprint].append(item)

        for fingerprint, items in by_fingerprint.items():
            if len(items) < 2:
                continue
            sections = sorted({item.parser_row.section for item in items})
            note = (
                f"Innehållsfingerprint {fingerprint[:12]} förekommer {len(items)} gånger "
                f"i paragraf(er): {', '.join(sections)}. Detta är inte automatiskt fel."
            )
            for item in items:
                if note not in item.comment:
                    item.comment = (item.comment + " " + note).strip()
