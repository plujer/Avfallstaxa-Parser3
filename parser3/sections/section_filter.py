"""Filters for false section headings."""

from __future__ import annotations

import re


class SectionFilter:
    DATE_RE = re.compile(r"20\d{2}[-./]\d{1,2}[-./]\d{1,2}")
    EWC_RE = re.compile(r"\b\d{6}\*?\b")

    def is_probably_false_heading(self, text: str) -> bool:
        clean = " ".join((text or "").split())
        lower = clean.lower()

        if self.DATE_RE.search(clean):
            return True
        if "förslag till taxestruktur" in lower and "§" not in lower:
            return True
        if self.EWC_RE.search(clean) and "§" not in lower:
            return True
        if lower.startswith("typ av avfall"):
            return True
        return False
