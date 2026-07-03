"""Generic rule engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RuleDecision:
    matched: bool
    rule: str = ""
    value: str = ""
    confidence: float = 0.0


class RuleEngine:
    def first_match(self, text: str, rules: list[tuple[str, str]]) -> RuleDecision:
        lower = (text or "").lower()
        for name, pattern in rules:
            if pattern.lower() in lower:
                return RuleDecision(True, name, pattern, 1.0)
        return RuleDecision(False, confidence=0.0)
