"""Detect informational rows."""

from __future__ import annotations


class InfoDetector:
    PHRASES = [
        "tömningskostnad",
        "för mer information",
        "omklassning sker",
        "debiteras",
        "beställning sker",
    ]

    def is_info(self, text: str) -> bool:
        lower = (text or "").lower()
        return any(phrase in lower for phrase in self.PHRASES)
