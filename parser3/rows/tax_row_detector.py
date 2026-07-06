"""Detect potential tax rows.

Precision rule:
A tax row must contain an explicit price marker. Words like "avgift", "kärl",
"tömning" or "fraktion" inside normal explanatory text are not enough.
"""

from __future__ import annotations

import re


class TaxRowDetector:
    PRICE_RE = re.compile(
        r"(?i)(?:\bXX+\s*kr\b|\b\d[\d\s]*,\d{2}\s*(?:kr)?\b|\b\d+\s*kr\b)"
    )

    SECTION_HEADING_RE = re.compile(r"^[1-9](?:\.\d+)*\s*§\s+")

    INFO_SENTENCE_MARKERS = [
        "är en ",
        "avses ",
        "innebär ",
        "gäller ",
        "ska ",
        "kan ",
        "får ",
        "enligt ",
        "definieras ",
        "bestämmelserna ",
        "förordningen ",
    ]

    def is_tax_candidate(self, text: str, row: list[str] | None = None) -> bool:
        row = row or []
        joined = " ".join(row) if row else (text or "")
        joined = " ".join((joined or "").replace("\xa0", " ").split())
        lower = joined.lower()

        if not joined:
            return False

        if self.SECTION_HEADING_RE.match(joined):
            return False

        if not self.PRICE_RE.search(joined):
            return False

        # Long explanatory paragraphs with only incidental price words must not export.
        if len(joined) > 180 and any(marker in lower for marker in self.INFO_SENTENCE_MARKERS):
            return False

        return True
