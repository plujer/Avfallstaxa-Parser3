"""Parse variant dimensions from tax code and supporting text."""

from __future__ import annotations

import re

from excel_builder.models import TaxVariantProfile
from excel_builder.taxcode.tax_code_parser import TaxCodeParser


class VariantParser:
    """Conservative parser for variants inside one tax family."""

    USAGE_HINTS = (
        ("FRITID", "FRITID"),
        ("FRITIDSHUS", "FRITID"),
        ("FRI", "FRITID"),
        ("VERKSAMHET", "VERKSAMHET"),
        ("PERMANENT", "PERMANENT"),
        ("EN- OCH TVÅBOSTAD", "SMÅHUS"),
        ("EN OCH TVÅBOSTAD", "SMÅHUS"),
        ("LÄGENHET", "LÄGENHET"),
    )

    WASTE_TEXT_HINTS = (
        ("REST-/MAT", "RM"),
        ("REST OCH MAT", "RM"),
        ("MAT OCH REST", "RM"),
        ("RESTAVFALL", "RE"),
        ("MATAVFALL", "MA"),
        ("PLAST", "PL"),
        ("PAPPER", "PA"),
        ("FÄRGAT GLAS", "GF"),
        ("OFÄRGAT GLAS", "GO"),
        ("METALL", "ME"),
        ("TIDNING", "TI"),
    )

    def __init__(self) -> None:
        self.tax_code_parser = TaxCodeParser()

    def parse(self, tax_code: str = "", source_text: str = "", source: str = "") -> TaxVariantProfile:
        parsed = self.tax_code_parser.parse(tax_code)
        text = self._normalize_text(source_text)

        volume = parsed.volume_liter or self._volume_from_text(text)
        waste = parsed.waste_code or self._waste_from_text(text)
        interval = parsed.interval or self._interval_from_text(text)
        variant = parsed.variant or self._variant_from_text(text)
        usage = self._usage_from_text(text) or self._usage_from_code_variant(variant)

        return TaxVariantProfile(
            tax_code=parsed.original_code,
            family_code=parsed.family_key,
            volume_liter=volume,
            waste_code=waste,
            interval=interval,
            variant=variant,
            usage_type=usage,
            source_text=source_text,
            source=source,
        )

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", str(text or "").strip().upper())

    def _volume_from_text(self, text: str) -> str:
        match = re.search(r"\b(\d{2,4})\s*(?:L|LITER|LITERS)\b", text)
        return match.group(1) if match else ""

    def _interval_from_text(self, text: str) -> str:
        match = re.search(r"\b(\d{1,3})\s*(?:DAG|DAGAR|GGR|GÅNGER)\b", text)
        return match.group(1) if match else ""

    def _waste_from_text(self, text: str) -> str:
        for needle, code in self.WASTE_TEXT_HINTS:
            if needle in text:
                return code
        return ""

    def _variant_from_text(self, text: str) -> str:
        if "EXTRA" in text:
            return "EX"
        if "LÅS" in text or "LAS" in text:
            return "LÅS"
        return ""

    def _usage_from_text(self, text: str) -> str:
        for needle, usage in self.USAGE_HINTS:
            if needle in text:
                return usage
        return ""

    def _usage_from_code_variant(self, variant: str) -> str:
        variant = str(variant or "").upper()
        if variant in {"FV", "FRI"}:
            return "FRITID"
        return ""
