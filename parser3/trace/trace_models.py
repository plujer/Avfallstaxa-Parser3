"""Trace models for parser diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TraceEvent:
    component: str
    section: str = ""
    input_text: str = ""
    normalized_text: str = ""
    best_match: str = ""
    score: float = 0.0
    decision: str = ""
    reason: str = ""
    order: int | None = None


@dataclass
class TraceStore:
    events: list[TraceEvent] = field(default_factory=list)

    def add(self, event: TraceEvent) -> None:
        self.events.append(event)

    def filter(self, component: str | None = None, section: str | None = None) -> list[TraceEvent]:
        result = self.events
        if component is not None:
            result = [event for event in result if event.component == component]
        if section is not None:
            result = [event for event in result if event.section == section]
        return result
