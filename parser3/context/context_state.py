"""Current semantic context while walking a document."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ContextState:
    chapter: str = ""
    section: str = ""
    section_title: str = ""
    group: str = ""
    header: str = ""

    def copy(self) -> "ContextState":
        return ContextState(
            chapter=self.chapter,
            section=self.section,
            section_title=self.section_title,
            group=self.group,
            header=self.header,
        )
