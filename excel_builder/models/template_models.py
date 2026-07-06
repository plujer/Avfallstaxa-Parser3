"""Models for versioned master workbook templates."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TemplateInfo:
    template_path: str
    version: str
    status: str
    output_path: str = ""
    warnings: list[str] = field(default_factory=list)

    @property
    def is_locked(self) -> bool:
        return self.status.lower() == "locked"
