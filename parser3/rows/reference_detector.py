"""Detect reference rows that should not be exported as tax rows."""

from __future__ import annotations


class ReferenceDetector:
    PHRASES = [
        "se farligt avfall",
        "se 6 §",
        "tillkommer enligt",
        "ingår i",
        "är kostnadsfritt",
    ]

    def is_reference(self, text: str) -> bool:
        lower = (text or "").lower()
        return any(phrase in lower for phrase in self.PHRASES)
