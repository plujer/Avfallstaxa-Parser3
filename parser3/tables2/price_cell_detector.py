"""Detect price cells without merging them into names."""

from __future__ import annotations

import re


class PriceCellDetector:
    PRICE_RE = re.compile(r"(?i)^(?:XX+|\d[\d\s]*,\d{2}|\d+)\s*kr$|^(?:XX+|\d[\d\s]*,\d{2})$")

    def is_price_cell(self, text: str) -> bool:
        clean = " ".join((text or "").replace("\xa0", " ").split())
        return bool(self.PRICE_RE.match(clean))

    def price_cells(self, cells: list[str]) -> list[tuple[int, str]]:
        return [(idx, cell.strip()) for idx, cell in enumerate(cells) if self.is_price_cell(cell)]
