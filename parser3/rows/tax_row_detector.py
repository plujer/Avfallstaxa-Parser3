"""Detect potential tax rows."""

from __future__ import annotations

import re


class TaxRowDetector:
    PRICE_RE = re.compile(r"\b(?:XX|XXX|XXXX|\d[\d\s]*,\d{2})\s*kr(?:/[a-zåäö]+)?\b", re.IGNORECASE)
    UNIT_WORDS = ["kilogram", "styck", "st", "liter", "m3", "m³", "besök", "tillfälle", "fraktion", "kg"]

    def is_tax_candidate(self, text: str, row: list[str] | None = None) -> bool:
        row = row or []
        joined = " ".join(row) if row else (text or "")
        lower = joined.lower()

        if self.PRICE_RE.search(joined):
            return True
        if any(unit in lower for unit in self.UNIT_WORDS) and len(joined.strip()) > 3:
            return True

        return False
