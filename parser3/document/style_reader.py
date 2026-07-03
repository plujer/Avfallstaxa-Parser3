"""Style helpers for Word blocks."""

from __future__ import annotations

import re


class StyleReader:
    """Detect heading styles and derive heading levels."""

    HEADING_RE = re.compile(r"heading\s*(\d+)", re.IGNORECASE)

    def is_heading(self, style_name: str) -> bool:
        return bool(self.HEADING_RE.search(style_name or ""))

    def heading_level(self, style_name: str) -> int | None:
        match = self.HEADING_RE.search(style_name or "")
        if not match:
            return None
        return int(match.group(1))
