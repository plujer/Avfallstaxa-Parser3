"""Rules for known section expectations."""

from __future__ import annotations


class SectionRuleEngine:
    VERIFIED_COUNTS = {
        "6.1.1": 6,
        "6.1.2": 103,
        "6.1.3": 4,
        "6.1.4": 4,
    }

    def expected_count(self, section: str) -> int | None:
        return self.VERIFIED_COUNTS.get(section)

    def is_verified_section(self, section: str) -> bool:
        return section in self.VERIFIED_COUNTS
