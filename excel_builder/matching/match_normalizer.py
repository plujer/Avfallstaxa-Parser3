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

    def row_key(self, section: str, tax_point: str, variant: str = "", unit: str = "") -> str:
        return "|".join([
            self.normalize(section),
            self.normalize(tax_point),
            self.normalize(variant),
            self.normalize(unit),
        ])

    def weak_key(self, section: str, tax_point: str) -> str:
        return "|".join([
            self.normalize(section),
            self.normalize(tax_point),
        ])
