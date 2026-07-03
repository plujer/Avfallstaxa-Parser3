"""Detect pseudo tables stored as paragraphs.

Some Word documents contain visually aligned rows as plain paragraphs instead of
real Word tables. This detector identifies common price-row patterns.
"""

from __future__ import annotations

import re

from parser3.document import DocumentBlock


class VisualTableDetector:
    PRICE_RE = re.compile(r"\b(?:XX|XXX|XXXX|\d[\d\s]*,\d{2})\s*kr\b", re.IGNORECASE)
    UNIT_RE = re.compile(r"\b(?:kg|kilogram|styck|st|liter|m3|m³|besök|tillfälle|fraktion)\b", re.IGNORECASE)

    def is_visual_table_row(self, block: DocumentBlock) -> bool:
        if block.kind != "paragraph":
            return False
        text = block.text or ""
        return bool(self.PRICE_RE.search(text) or self.UNIT_RE.search(text))

    def collect_runs(self, blocks: list[DocumentBlock]) -> list[list[DocumentBlock]]:
        runs: list[list[DocumentBlock]] = []
        current: list[DocumentBlock] = []

        for block in blocks:
            if self.is_visual_table_row(block):
                current.append(block)
            else:
                if len(current) >= 2:
                    runs.append(current)
                current = []

        if len(current) >= 2:
            runs.append(current)

        return runs
