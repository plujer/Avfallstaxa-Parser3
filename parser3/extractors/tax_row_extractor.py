"""Extract TaxRow objects from classified rows.

This extractor now delegates single-cell visual rows to FlatTaxExtractor so price
markers are not kept inside the name.
"""

from __future__ import annotations

import re

from parser3.extractors.flat_tax_extractor import FlatTaxExtractor
from parser3.extractors.metadata_extractor import MetadataExtractor
from parser3.models import TaxRow
from parser3.rows import RowClassifier
from parser3.taxonomy import UnitDetector, VariantBuilder
from parser3.utils.constants import ROW_TYPE_TAX


class TaxRowExtractor:
    PRICE_RE = re.compile(r"(?i)(XX+\s*kr|\d[\d\s]*,\d{2}\s*(?:kr)?|\d+\s*kr)")

    def __init__(self) -> None:
        self.classifier = RowClassifier()
        self.unit_detector = UnitDetector()
        self.variant_builder = VariantBuilder()
        self.metadata_extractor = MetadataExtractor()
        self.flat_extractor = FlatTaxExtractor()

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
            non_empty = [c for c in row if (c or "").strip()]
            if len(non_empty) == 1:
                result.extend(
                    self.flat_extractor.extract_line(
                        non_empty[0],
                        chapter=chapter,
                        section=section,
                        group=group,
                    )
                )
                continue

            classified = self.classifier.classify(row)
            if classified.row_type != ROW_TYPE_TAX:
                continue

            name = self._name_from_row(row)
            if not name:
                continue

            prices = [m.group(1).strip() for m in self.PRICE_RE.finditer(" ".join(row))]
            if not prices:
                continue

            for price in prices:
                result.append(
                    TaxRow(
                        chapter=chapter,
                        section=section,
                        group=group,
                        name=name,
                        variant=self.variant_builder.from_context(group, header, row),
                        unit=self.unit_detector.detect(row, classified.text),
                        price=price,
                        ewc=self.metadata_extractor.extract_ewc(row),
                        un_number=self.metadata_extractor.extract_un(row),
                        export=True,
                    )
                )

        return result

    def _name_from_row(self, row: list[str]) -> str:
        for cell in row:
            clean = (cell or "").strip()
            if not clean:
                continue
            if clean.lower().startswith(("ewc", "un-nr", "enhet", "pris")):
                continue
            if self.PRICE_RE.fullmatch(clean):
                continue
            return self.PRICE_RE.sub("", clean).strip(" -–—:;,.")
        return ""
