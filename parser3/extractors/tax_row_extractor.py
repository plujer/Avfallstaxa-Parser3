"""Extract TaxRow objects from classified table rows."""

from __future__ import annotations

import re

from parser3.models import TaxRow
from parser3.rows import RowClassifier
from parser3.taxonomy import UnitDetector, VariantBuilder
from parser3.extractors.metadata_extractor import MetadataExtractor
from parser3.utils.constants import ROW_TYPE_TAX


class TaxRowExtractor:
    PRICE_RE = re.compile(r"(?i)(XX+\s*kr|\d[\d\s]*,\d{2}\s*(?:kr)?|\d+\s*kr)")

    def __init__(self) -> None:
        self.classifier = RowClassifier()
        self.unit_detector = UnitDetector()
        self.variant_builder = VariantBuilder()
        self.metadata_extractor = MetadataExtractor()

    def extract_from_rows(
        self,
        rows: list[list[str]],
        chapter: str = "",
        section: str = "",
        group: str = "",
        header: str = "",
    ) -> list[TaxRow]:
        result: list[TaxRow] = []

        for row in rows:
            classified = self.classifier.classify(row)
            if classified.row_type != ROW_TYPE_TAX:
                continue

            name = self._name_from_row(row)
            if not name:
                continue

            result.append(
                TaxRow(
                    chapter=chapter,
                    section=section,
                    group=group,
                    name=name,
                    variant=self.variant_builder.from_context(group, header, row),
                    unit=self.unit_detector.detect(row, classified.text),
                    price=self._price_from_row(row),
                    ewc=self.metadata_extractor.extract_ewc(row),
                    un_number=self.metadata_extractor.extract_un(row),
                    export=True,
                )
            )

        return result

    def _name_from_row(self, row: list[str]) -> str:
        # Prefer first non-empty cell that is not only a price.
        for cell in row:
            clean = (cell or "").strip()
            if not clean:
                continue
            if clean.lower().startswith(("ewc", "un-nr", "enhet", "pris")):
                continue
            if self.PRICE_RE.fullmatch(clean):
                continue
            return clean
        return ""

    def _price_from_row(self, row: list[str]) -> str:
        for cell in reversed(row):
            clean = (cell or "").strip()
            match = self.PRICE_RE.search(clean)
            if match:
                return match.group(1).strip()
        return ""
