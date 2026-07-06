"""Normalization used only for Excel Builder matching.

This must not change source values. It only creates comparison keys.
"""

from __future__ import annotations

import re


class MatchNormalizer:
    def normalize(self, value: str) -> str:
        text = str(value or "").replace("\xa0", " ")
        text = text.replace("–", "-").replace("—", "-").replace("×", "x").replace("*", "x")
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"\s*/\s*", "/", text)
        text = re.sub(r"\s*-\s*", "-", text)
        text = re.sub(r"\s*x\s*", "x", text)
        text = text.strip(" .;:")
        return text

    def normalize_section(self, value: str) -> str:
        """Normalize paragraph/section numbers for matching.

        Examples:
        - "§2.1" -> "2.1"
        - "§ 6.1.2" -> "6.1.2"
        - "6.1.2 " -> "6.1.2"
        """
        text = self.normalize(value)
        text = text.replace("§", "").strip()
        text = re.sub(r"^paragraf\s+", "", text)
        text = re.sub(r"^avsnitt\s+", "", text)
        text = text.strip(" .;:")
        return text

    def row_key(self, section: str, tax_point: str, variant: str = "", unit: str = "") -> str:
        return "|".join([
            self.normalize_section(section),
            self.normalize(tax_point),
            self.normalize(variant),
            self.normalize(unit),
        ])

    def weak_key(self, section: str, tax_point: str) -> str:
        return "|".join([
            self.normalize_section(section),
            self.normalize(tax_point),
        ])
