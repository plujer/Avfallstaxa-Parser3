"""Extract tax rows from visually formatted paragraph rows."""

from __future__ import annotations

import re

from parser3.models import TaxRow
from parser3.taxonomy.unit_detector import UnitDetector


class FlatTaxExtractor:
    PRICE_RE = re.compile(r"(?i)(XX+\s*kr|\d[\d\s]*,\d{2}\s*(?:kr)?|\d+\s*kr)")
    BAD_NOTE_RE = re.compile(r"(?i)tillkommer\s+XX+\s*kr\s+eller\s+%")
    STARTS_LOWER_RE = re.compile(r"^[a-zåäö]")
    UNIT_SUFFIX_RE = re.compile(
        r"(?i)\s*/\s*(fraktion|besök|tillfälle|kärl|container|dygn|vecka|år|tömning|budning|bunt|säck)\s*$"
    )

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

        if self.STARTS_LOWER_RE.match(clean):
            return []

        prices = [m.group(1).strip() for m in self.PRICE_RE.finditer(clean)]
        if not prices:
            return []

        name = self._name_without_prices(clean)
        name, suffix_unit = self._split_unit_suffix(name)
        if not name:
            return []

        detected_unit = suffix_unit or self.unit_detector.detect([name], clean)

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
                    unit=detected_unit,
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

    def _split_unit_suffix(self, name: str) -> tuple[str, str]:
        match = self.UNIT_SUFFIX_RE.search(name)
        if not match:
            return name, ""
        unit = match.group(1).lower()
        clean_name = self.UNIT_SUFFIX_RE.sub("", name).strip(" -–—:;,.")
        return clean_name, unit

    def _clean(self, text: str) -> str:
        return " ".join((text or "").replace("\xa0", " ").split())
