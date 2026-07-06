"""Acceptance test models for parser verification against manually verified facit."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AcceptanceExpectation:
    section: str
    expected_count: int
    ignored_names: list[str] = field(default_factory=list)
    required_names: list[str] = field(default_factory=list)


@dataclass
class SectionAcceptanceResult:
    section: str
    expected_count: int
    actual_count: int
    passed: bool
    missing_required: list[str] = field(default_factory=list)
    wrongly_exported_ignored: list[str] = field(default_factory=list)


@dataclass
class AcceptanceResult:
    sections: list[SectionAcceptanceResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(section.passed for section in self.sections)

    @property
    def expected_total(self) -> int:
        return sum(section.expected_count for section in self.sections)

    @property
    def actual_total(self) -> int:
        return sum(section.actual_count for section in self.sections)
