"""Robust section classifier for Parser 3.0.

Rules:
- Accept real tariff section headings such as:
  2 § Grundavgift
  2.5.1 § Budning...
  6.1.2 § Hanteringsavgifter...
- Reject years, dates, EWC codes, UN numbers, prices and normal data rows.
"""

from __future__ import annotations

import re

from parser3.headings.heading import HeadingMatch


class SectionClassifier:
    SECTION_RE = re.compile(
        r"^(?P<number>[1-9](?:\.\d{1,2}){0,3})\s*§\s*(?P<title>.+?)\s*$"
    )

    # fallback allows headings without §, but only if title looks like a real heading
    FALLBACK_RE = re.compile(
        r"^(?P<number>[1-9](?:\.\d{1,2}){0,3})\s+(?P<title>[A-ZÅÄÖa-zåäö].{3,})$"
    )

    DATE_RE = re.compile(r"\b20\d{2}[-./]\d{1,2}[-./]\d{1,2}\b")
    YEAR_RE = re.compile(r"^20\d{2}$")
    EWC_RE = re.compile(r"^\d{6}\*?$")
    UN_RE = re.compile(r"^\d{4}$")
    PRICE_RE = re.compile(r"\b\d+[\s\d]*,\d{2}\b|\b(?:XX|XXX|XXXX)\s*kr\b", re.IGNORECASE)

    FORBIDDEN_STARTS = (
        "avfall till",
        "container x",
        "kärl ",
        "batterier",
        "toner",
        "asbest",
        "diesel",
        "bensin",
        "fönster",
        "plast",
    )

    def classify(self, text: str) -> HeadingMatch | None:
        clean = self._clean(text)
        if not clean or self._is_forbidden(clean):
            return None

        match = self.SECTION_RE.match(clean)
        if not match:
            match = self.FALLBACK_RE.match(clean)

        if not match:
            return None

        number = match.group("number")
        title = match.group("title").strip()

        if not self._valid_number(number):
            return None

        if not self._valid_title(title):
            return None

        return HeadingMatch(
            number=number,
            title=title,
            level=number.count(".") + 1,
            raw_text=clean,
        )

    def _clean(self, text: str) -> str:
        return " ".join((text or "").replace("\xa0", " ").split())

    def _valid_number(self, number: str) -> bool:
        if self.YEAR_RE.fullmatch(number):
            return False
        if self.EWC_RE.fullmatch(number):
            return False
        if self.UN_RE.fullmatch(number):
            return False

        parts = number.split(".")
        if len(parts) > 4:
            return False

        # Main tariff chapters are 1-9 in this document.
        first = int(parts[0])
        if first < 1 or first > 9:
            return False

        # Avoid dates like 2026.03.13 and odd large components.
        for part in parts:
            if len(part) > 2:
                return False
            if int(part) > 99:
                return False

        return True

    def _valid_title(self, title: str) -> bool:
        lower = title.lower().strip()
        if not title or len(title) < 3:
            return False
        if self.PRICE_RE.search(title):
            return False
        if self.DATE_RE.search(title):
            return False
        if self.EWC_RE.fullmatch(title):
            return False
        if self.UN_RE.fullmatch(title):
            return False
        if lower.startswith(self.FORBIDDEN_STARTS):
            return False
        return True

    def _is_forbidden(self, text: str) -> bool:
        lower = text.lower().strip()
        if self.YEAR_RE.fullmatch(lower):
            return True
        if self.DATE_RE.search(lower):
            return True
        if self.EWC_RE.fullmatch(lower):
            return True
        if self.UN_RE.fullmatch(lower):
            return True
        if self.PRICE_RE.search(lower) and "§" not in lower:
            return True
        return False
