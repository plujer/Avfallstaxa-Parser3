"""Name normalization for acceptance comparison.

This layer is only for comparing parser output with facit. It must not change the
source Word text or the generated Excel rows.
"""

from __future__ import annotations

import re


class NameNormalizer:
    ALIASES = {
        "förpackningar, tömde ej rengjorda": "förpackningar, tömda ej rengjorda",
        "gasol inkl tub": "gasol inkl. tub",
        "flourvätesyra": "fluorvätesyra",
        "surt oorganisk fast ämne": "surt oorganiskt fast ämne",
        "surt organisk fast ämne": "surt organiskt fast ämne",
        "rengöring/vaskmedel fast": "rengörings-/vaskmedel fast",
        "färg-,lack-, limburkar vattenbaserade": "färg-, lack-, limburkar vattenbaserade",
        "härdare metyl- etylketonperoxid": "härdare metyl-etylketonperoxid",
        "oljeavfall, fast osorterat emba": "oljeavfall, fast osorterat emballage",
        "wc stol": "wc-stol",
        "stubbar rötter för krossning": "stubbar/rötter för krossning",
    }

    UNIT_WORDS = {
        "kilogram", "kg", "liter", "l", "m³", "m3", "styck", "st", "ton", "container",
        "dygn", "vecka", "år", "tömning", "besök", "budning", "bunt", "säck",
    }

    def normalize(self, value: str) -> str:
        text = (value or "").replace("\xa0", " ")
        text = text.replace("–", "-").replace("—", "-")
        text = text.replace("×", "x").replace("*", "x")
        text = text.lower().strip()

        text = self._remove_metadata_tokens(text)
        text = self._remove_trailing_price(text)

        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"\s*/\s*", "/", text)
        text = re.sub(r"\s*-\s*", "-", text)
        text = re.sub(r"\s*x\s*", "x", text)
        text = text.replace("m3", "m³")
        text = text.replace(" inkl ", " inkl. ")
        text = re.sub(r"\binkl\.\.", "inkl.", text)

        text = self._remove_trailing_units(text)
        text = self._collapse_duplicate_halves(text)

        text = text.strip(" .;:")
        text = self.ALIASES.get(text, text)
        return text

    def _remove_metadata_tokens(self, text: str) -> str:
        # Remove EWC codes and UN numbers that can be appended to table text.
        text = re.sub(r"\b\d{6}\*?\b", " ", text)
        text = re.sub(r"\bun[- ]?nr\b", " ", text)
        text = re.sub(r"\bewc(?: kod)?\b", " ", text)

        # Remove common UN numbers when they stand alone after a row.
        text = re.sub(r"\b\d{4}\b", " ", text)
        return text

    def _remove_trailing_price(self, text: str) -> str:
        return re.sub(r"(?i)\b(?:xx+|\d[\d\s]*,\d{2}|\d+)\s*kr\b", " ", text)

    def _remove_trailing_units(self, text: str) -> str:
        parts = text.split()
        while parts and parts[-1].strip(".,;:") in self.UNIT_WORDS:
            parts.pop()
        return " ".join(parts)

    def _collapse_duplicate_halves(self, text: str) -> str:
        # Word tables sometimes duplicate cell content in parsed text.
        parts = text.split()
        if len(parts) % 2 != 0 or not parts:
            return text
        half = len(parts) // 2
        if parts[:half] == parts[half:]:
            return " ".join(parts[:half])
        return text
