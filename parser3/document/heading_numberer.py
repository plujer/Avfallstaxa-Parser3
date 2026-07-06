"""Generate visible section numbers from Word heading styles.

The source Word document uses automatic heading numbering. python-docx returns
paragraph.text without that numbering. This module reconstructs numbering from
Heading 1, Heading 2, Heading 3, ... styles.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class HeadingNumberer:
    counters: list[int] = field(default_factory=lambda: [0] * 9)

    HEADING_RE = re.compile(r"heading\s*(\d+)", re.IGNORECASE)

    def level_from_style(self, style_name: str) -> int | None:
        match = self.HEADING_RE.search(style_name or "")
        if not match:
            return None
        level = int(match.group(1))
        if level < 1 or level > len(self.counters):
            return None
        return level

    def next_number(self, level: int) -> str:
        self.counters[level - 1] += 1

        for idx in range(level, len(self.counters)):
            self.counters[idx] = 0

        # If a lower heading appears before a parent, initialize parents to 1.
        for idx in range(level - 1):
            if self.counters[idx] == 0:
                self.counters[idx] = 1

        return ".".join(str(part) for part in self.counters[:level] if part > 0)

    def prefix_heading(self, text: str, style_name: str) -> tuple[str, dict]:
        level = self.level_from_style(style_name)
        if level is None:
            return text, {}

        number = self.next_number(level)
        clean = " ".join((text or "").replace("\xa0", " ").split())

        # Do not double-prefix headings that already contain a section number.
        if re.match(r"^[1-9](?:\.\d+)*\s*§", clean):
            return clean, {"heading_level": level, "section_number": number, "original_text": clean}

        prefixed = f"{number} § {clean}"
        return prefixed, {
            "heading_level": level,
            "section_number": number,
            "original_text": clean,
            "generated_heading_number": True,
        }
