"""Extract semantic attributes from tax text.

The extractor is intentionally conservative. It only emits attributes when it
finds explicit, well-known Swedish waste/tax terms in the supplied text.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from excel_builder.models import SemanticAttributeProfile


class SemanticAttributeExtractor:
    MATERIAL_HINTS: tuple[tuple[str, str], ...] = (
        ("ASBEST", "ASBEST"),
        ("TRÄ", "TRÄ"),
        ("TRA", "TRÄ"),
        ("JORD", "JORD"),
        ("STEN", "STEN"),
        ("STUBB", "STUBBAR/RÖTTER"),
        ("RÖTTER", "STUBBAR/RÖTTER"),
        ("ROTTER", "STUBBAR/RÖTTER"),
        ("GLAS", "GLAS"),
        ("METALL", "METALL"),
        ("PLAST", "PLAST"),
        ("PAPPER", "PAPPER"),
        ("GIPS", "GIPS"),
        ("DÄCK", "DÄCK"),
        ("DACK", "DÄCK"),
    )

    WASTE_HINTS: tuple[tuple[str, str], ...] = (
        ("REST-/MAT", "REST/MAT"),
        ("REST OCH MAT", "REST/MAT"),
        ("MAT OCH REST", "REST/MAT"),
        ("RESTAVFALL", "REST"),
        ("MATAVFALL", "MAT"),
        ("FÄRGAT GLAS", "FÄRGAT GLAS"),
        ("OFÄRGAT GLAS", "OFÄRGAT GLAS"),
        ("FARLIGT AVFALL", "FARLIGT AVFALL"),
        ("GROVAVFALL", "GROVAVFALL"),
        ("TRÄDGÅRDSAVFALL", "TRÄDGÅRDSAVFALL"),
        ("TRADGARDSAVFALL", "TRÄDGÅRDSAVFALL"),
        ("TIDNING", "TIDNING"),
    )

    CONTAINER_HINTS: tuple[tuple[str, str], ...] = (
        ("KÄRL", "KÄRL"),
        ("KARL", "KÄRL"),
        ("CONTAINER", "CONTAINER"),
        ("SÄCK", "SÄCK"),
        ("SACK", "SÄCK"),
        ("FACK", "FACK"),
        ("BOX", "BOX"),
    )

    PROPERTY_HINTS: tuple[tuple[str, str], ...] = (
        ("FRITIDSHUS", "FRITIDSHUS"),
        ("FRITID", "FRITIDSHUS"),
        ("VERKSAMHET", "VERKSAMHET"),
        ("LÄGENHET", "LÄGENHET"),
        ("LAGENHET", "LÄGENHET"),
        ("EN- OCH TVÅBOSTAD", "SMÅHUS"),
        ("EN OCH TVÅBOSTAD", "SMÅHUS"),
        ("SMÅHUS", "SMÅHUS"),
        ("SMAHUS", "SMÅHUS"),
        ("CAMPING", "CAMPING"),
    )

    UNIT_PATTERNS: tuple[tuple[str, str], ...] = (
        (r"\bKR\s*/\s*KG\b|\bKR PER KG\b|\bKG\b", "KG"),
        (r"\bKR\s*/\s*TON\b|\bKR PER TON\b|\bTON\b", "TON"),
        (r"\bM3\b|\bM³\b|\bKUBIK\b", "M3"),
        (r"\bL\b|\bLITER\b", "LITER"),
        (r"\bFRaktion\b", "FRAKTION"),
        (r"\bBES[ÖO]K\b", "BESÖK"),
        (r"\bH[ÄA]MTNING\b", "HÄMTNING"),
    )

    def extract(self, tax_code: str = "", text: str = "", source: str = "") -> SemanticAttributeProfile:
        normalized = self._normalize(text)
        return SemanticAttributeProfile(
            tax_code=str(tax_code or "").strip(),
            source_text=text,
            source=source,
            materials=self._find_hints(normalized, self.MATERIAL_HINTS),
            waste_types=self._find_hints(normalized, self.WASTE_HINTS),
            units=self._find_units(normalized),
            container_types=self._find_hints(normalized, self.CONTAINER_HINTS),
            intervals=self._find_intervals(normalized),
            property_types=self._find_hints(normalized, self.PROPERTY_HINTS),
        )

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", str(text or "").strip().upper())

    def _find_hints(self, text: str, hints: Iterable[tuple[str, str]]) -> tuple[str, ...]:
        values: list[str] = []
        for needle, value in hints:
            if needle.upper() in text and value not in values:
                values.append(value)
        return tuple(values)

    def _find_units(self, text: str) -> tuple[str, ...]:
        values: list[str] = []
        for pattern, value in self.UNIT_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE) and value not in values:
                values.append(value)
        return tuple(values)

    def _find_intervals(self, text: str) -> tuple[str, ...]:
        values: list[str] = []
        for match in re.finditer(r"\b(\d{1,3})\s*(DAGAR|DAG|GGR|GÅNGER|GANGER)\b", text):
            value = f"{match.group(1)} {match.group(2).replace('GANGER', 'GÅNGER')}"
            if value not in values:
                values.append(value)
        return tuple(values)
