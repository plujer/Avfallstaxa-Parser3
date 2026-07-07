"""Deterministic mapping from Word/parser tax rows to Taxepunkter rows.

The engine is a traceability layer. It does not decide whether an EDP tax code is
right or wrong and it does not treat repeated EDP tax codes as errors. The core
invariant is that each Word tax row must be represented in Taxepunkter.

Block50 adds two identities per Word tax row:
- ``word_tax_id``: section-aware ID used for exact traceability to the current
  Word master structure.
- ``stable_tax_identity``: section-independent content identity used to detect
  when a tax point has moved in the Word document without changing its meaning.
"""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict

from excel_builder.matching import MatchNormalizer
from excel_builder.models import ParserTaxRow, WorkbookTaxRow
from excel_builder.models.word_excel_mapping_models import WordExcelMappingItem, WordExcelMappingReport


class WordExcelMappingEngine:
    """Create stable traceability IDs and map Word tax rows to Excel rows."""

    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def build(self, parser_rows: list[ParserTaxRow], workbook_rows: list[WorkbookTaxRow]) -> WordExcelMappingReport:
        report = WordExcelMappingReport()
        exact_index: dict[str, list[WorkbookTaxRow]] = defaultdict(list)
        weak_index: dict[str, list[WorkbookTaxRow]] = defaultdict(list)

        for workbook_row in workbook_rows:
            exact_index[self._exact_key(workbook_row)].append(workbook_row)
            weak_index[self._weak_key(workbook_row)].append(workbook_row)

        occurrence_count: dict[str, int] = defaultdict(int)
        stable_occurrence_count: dict[str, int] = defaultdict(int)
        for ordinal, parser_row in enumerate(parser_rows, start=1):
            identity_key = self._identity_key(parser_row)
            occurrence_count[identity_key] += 1
            word_tax_id = self._word_tax_id(parser_row, occurrence_count[identity_key])

            stable_identity_key = self._stable_identity_key(parser_row)
            stable_occurrence_count[stable_identity_key] += 1
            stable_tax_identity = self._stable_tax_identity(parser_row)
            content_fingerprint = self._content_fingerprint(parser_row)

            exact_matches = exact_index.get(self._exact_key(parser_row), [])
            if len(exact_matches) == 1:
                report.items.append(
                    self._item(
                        word_tax_id,
                        stable_tax_identity,
                        content_fingerprint,
                        parser_row,
                        exact_matches[0],
                        "MAPPED",
                        "exact row",
                        1.0,
                        "Word-raden har exakt motsvarande rad i Taxepunkter.",
                    )
                )
                continue

            if len(exact_matches) > 1:
                report.items.append(
                    self._item(
                        word_tax_id,
                        stable_tax_identity,
                        content_fingerprint,
                        parser_row,
                        exact_matches[0],
                        "REVIEW",
                        "duplicate exact Taxepunkter rows",
                        0.85,
                        (
                            f"{len(exact_matches)} Excel-rader matchar samma Word-rad. "
                            "Detta är granskningsläge, inte automatiskt fel."
                        ),
                    )
                )
                continue

            weak_matches = weak_index.get(self._weak_key(parser_row), [])
            if len(weak_matches) == 1:
                report.items.append(
                    self._item(
                        word_tax_id,
                        stable_tax_identity,
                        content_fingerprint,
                        parser_row,
                        weak_matches[0],
                        "MAPPED",
                        "section+tax_point",
                        0.75,
                        "Word-raden finns i Taxepunkter men variant eller enhet skiljer.",
                    )
                )
                continue

            if len(weak_matches) > 1:
                report.items.append(
                    self._item(
                        word_tax_id,
                        stable_tax_identity,
                        content_fingerprint,
                        parser_row,
                        weak_matches[0],
                        "REVIEW",
                        "multiple section+tax_point rows",
                        0.6,
                        (
                            f"{len(weak_matches)} Excel-rader delar paragraf och taxepunkt. "
                            "Kräver granskning men är inte automatiskt fel."
                        ),
                    )
                )
                continue

            report.items.append(
                self._item(
                    word_tax_id,
                    stable_tax_identity,
                    content_fingerprint,
                    parser_row,
                    None,
                    "MISSING",
                    "no Taxepunkter row",
                    0.0,
                    "Word-raden saknar motsvarande rad i Taxepunkter.",
                )
            )

        self._add_duplicate_edp_notes(report)
        self._add_moved_tax_notes(report)
        return report

    def _item(
        self,
        word_tax_id: str,
        stable_tax_identity: str,
        content_fingerprint: str,
        parser_row: ParserTaxRow,
        workbook_row: WorkbookTaxRow | None,
        status: str,
        method: str,
        confidence: float,
        comment: str,
    ) -> WordExcelMappingItem:
        return WordExcelMappingItem(
            word_tax_id=word_tax_id,
            stable_tax_identity=stable_tax_identity,
            content_fingerprint=content_fingerprint,
            parser_row=parser_row,
            workbook_row=workbook_row,
            status=status,
            method=method,
            confidence=confidence,
            comment=comment,
        )

    def _exact_key(self, row: ParserTaxRow | WorkbookTaxRow) -> str:
        return self.normalizer.row_key(row.section, row.tax_point, row.variant, row.unit)

    def _weak_key(self, row: ParserTaxRow | WorkbookTaxRow) -> str:
        return self.normalizer.weak_key(row.section, row.tax_point)

    def _identity_key(self, row: ParserTaxRow) -> str:
        return "|".join([row.section, row.tax_point, row.variant, row.unit])

    def _stable_identity_key(self, row: ParserTaxRow) -> str:
        """Identity independent of paragraph number/section.

        This makes it possible to detect moved Word tax rows between master
        versions. The section-aware ``word_tax_id`` remains the exact trace ID for
        the current master, while this key remains stable if the tax text is moved
        to a different paragraph.
        """
        return self.normalizer.row_key("", row.tax_point, row.variant, row.unit)

    def _word_tax_id(self, row: ParserTaxRow, occurrence: int) -> str:
        raw = self._identity_key(row)
        digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8].upper()
        section = re.sub(r"[^0-9A-Za-z]+", "-", row.section).strip("-") or "NOSECTION"
        return f"WTX-{section}-{digest}-{occurrence:02d}"

    def _stable_tax_identity(self, row: ParserTaxRow) -> str:
        raw = self._stable_identity_key(row)
        digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10].upper()
        return f"WTX-STABLE-{digest}"

    def _content_fingerprint(self, row: ParserTaxRow) -> str:
        raw = self._stable_identity_key(row)
        return hashlib.sha1(raw.encode("utf-8")).hexdigest().upper()

    def _add_duplicate_edp_notes(self, report: WordExcelMappingReport) -> None:
        by_tax_code: dict[str, list[WordExcelMappingItem]] = defaultdict(list)
        for item in report.items:
            if item.workbook_row and item.workbook_row.tax_code:
                by_tax_code[item.workbook_row.tax_code].append(item)

        for tax_code, items in by_tax_code.items():
            if len(items) < 2:
                continue
            for item in items:
                suffix = (
                    f" Samma EDP-taxa ({tax_code}) används av {len(items)} Word-rader. "
                    "Det är tillåtet och ska inte klassas som fel utan annan konflikt."
                )
                if suffix.strip() not in item.comment:
                    item.comment = (item.comment + suffix).strip()

    def _add_moved_tax_notes(self, report: WordExcelMappingReport) -> None:
        """Annotate rows that share content identity but appear in several sections."""
        by_stable_id: dict[str, list[WordExcelMappingItem]] = defaultdict(list)
        for item in report.items:
            by_stable_id[item.stable_tax_identity].append(item)

        for stable_id, items in by_stable_id.items():
            sections = {item.parser_row.section for item in items}
            if len(items) < 2 or len(sections) < 2:
                continue
            for item in items:
                suffix = (
                    f" Stabil identitet {stable_id} förekommer i flera paragrafer. "
                    "Det kan betyda flyttad/återanvänd taxepunkt och är granskningsinformation, inte automatiskt fel."
                )
                if suffix.strip() not in item.comment:
                    item.comment = (item.comment + suffix).strip()
