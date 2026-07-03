"""Metadata extraction for table rows."""

from __future__ import annotations

import re


class MetadataExtractor:
    # Important: no word boundary after optional *, because * is not a word char.
    EWC_RE = re.compile(r"(?<!\d)(\d{6}\*?)(?!\d)")
    UN_RE = re.compile(r"(?<!\d)(\d{4})(?!\d)")

    def extract_ewc(self, cells: list[str]) -> str:
        """Return EWC code including optional trailing asterisk."""
        for cell in cells:
            match = self.EWC_RE.search(cell or "")
            if match:
                return match.group(1)
        return ""

    def extract_un(self, cells: list[str]) -> str:
        """Return UN number, without confusing it with an EWC code."""
        for cell in cells:
            value = cell or ""
            if self.EWC_RE.search(value):
                continue
            match = self.UN_RE.search(value)
            if match:
                return match.group(1)
        return ""
