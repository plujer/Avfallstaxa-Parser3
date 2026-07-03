"""Classify paragraph text as numbered sections."""

from __future__ import annotations

import re

from parser3.headings.heading import HeadingMatch


class SectionClassifier:
    """Detect section numbers like 2 §, 2.2.4 §, 6.1.2 §."""

    SECTION_RE = re.compile(
        r"^(?P<number>\d+(?:\.\d+)*)\s*§?\s*(?P<title>.+?)\s*$"
    )

    def classify(self, text: str) -> HeadingMatch | None:
        clean = " ".join((text or "").replace("\xa0", " ").split())
        match = self.SECTION_RE.match(clean)
        if not match:
            return None

        number = match.group("number")
        title = match.group("title").strip()
        level = number.count(".") + 1

        return HeadingMatch(
            number=number,
            title=title,
            level=level,
            raw_text=clean,
        )
