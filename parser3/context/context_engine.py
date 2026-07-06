"""High-level context engine for Parser 3.0."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from parser3.context.section_context_assigner import SectionContextAssigner
from parser3.document import DocumentBlock


@dataclass
class ContextSummary:
    section_counts: dict[str, int]


class ContextEngine:
    def __init__(self) -> None:
        self.assigner = SectionContextAssigner()

    def assign(self, blocks: list[DocumentBlock]):
        return self.assigner.assign(blocks)

    def summary(self, blocks: list[DocumentBlock]) -> ContextSummary:
        assigned = self.assign(blocks)
        counts = Counter(cb.context.section for cb in assigned if cb.context.section)
        return ContextSummary(section_counts=dict(sorted(counts.items())))
