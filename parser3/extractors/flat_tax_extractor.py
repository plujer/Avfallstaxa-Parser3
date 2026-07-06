"""Extract tax rows from visually formatted paragraph rows.

Many source documents look like tables on the page, but python-docx receives them
as normal paragraphs. This extractor handles rows such as:

    Fritidshus XX kr
    Kärl 240 l (mat-/restavfall) XX kr XX kr XX kr

and keeps the name separate from the price markers.
"""

from __future__ import annotations

import re

from parser3.models import TaxRow
from parser3.taxonomy.unit_detector import UnitDetector


class FlatTaxExtractor:
    PRICE_RE = re.compile(r"(?i)(XX+\s*kr|\d[\d\s]*,\d{2}\s*(?:kr)?|\d+\s*kr)")
    BAD_NOTE_RE = re.compile(r"(?i)tillkommer\s+XX+\s*kr\s+eller\s+%")
    STARTS_LOWER_RE = re.compile(r"^[a-zåäö]")

    def __init__(self) -> None:
        self.unit_detector = UnitDetector()

    def extract_line(
        self,
        text: str,
        chapter: str = "",
        section: str = "",
        group: str = "",
        variants: list[str] | None = None,
    ) -> list[TaxRow]:
        clean = self._clean(text)
        if not clean:
            return []

        if self.BAD_NOTE_RE.search(clean):
            return []

        # Most orphan continuation fragments start lowercase and should not become tax rows.
        if self.STARTS_LOWER_RE.match(clean):
            return []

        prices = [m.group(1).strip() for m in self.PRICE_RE.finditer(clean)]
        if not prices:
            return []

        name = self._name_without_prices(clean)
        if not name:
            return []

        variants = variants or []
        rows: list[TaxRow] = []
        for idx, price in enumerate(prices):
            variant = variants[idx] if idx < len(variants) else ""
            rows.append(
                TaxRow(
                    chapter=chapter,
                    section=section,
                    group=group,
                    name=name,
                    variant=variant,
                    unit=self.unit_detector.detect([name], clean),
                    price=price,
                    export=True,
                )
            )
        return rows

    def _name_without_prices(self, text: str) -> str:
        name = self.PRICE_RE.sub("", text)
        name = re.sub(r"\s+", " ", name)
        name = name.strip(" -–—:;,.")
        return name.strip()

    def _clean(self, text: str) -> str:
        return " ".join((text or "").replace("\\xa0", " ").split())
