"""Rulebook models for Excel Builder."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RuleEntry:
    source_sheet: str
    row_number: int
    key: str
    text: str
    status: str = ""


@dataclass
class Rulebook:
    entries: list[RuleEntry] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.entries)

    def contains_text(self, needle: str) -> bool:
        needle_norm = self._norm(needle)
        return any(needle_norm in self._norm(entry.text) for entry in self.entries)

    def entries_from(self, sheet_name: str) -> list[RuleEntry]:
        return [entry for entry in self.entries if entry.source_sheet == sheet_name]

    def _norm(self, value: str) -> str:
        return " ".join(str(value or "").replace("\xa0", " ").lower().split())
