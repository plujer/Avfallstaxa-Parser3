"""Rules for rows that are references, not taxes."""

from __future__ import annotations


class ReferenceRuleEngine:
    REFERENCES = [
        "se farligt avfall",
        "se taxa",
        "se paragraf",
        "se 6 §",
    ]

    def is_reference(self, text: str) -> bool:
        lower = (text or "").lower()
        return any(ref in lower for ref in self.REFERENCES)
