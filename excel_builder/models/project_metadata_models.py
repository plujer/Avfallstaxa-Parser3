from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProjectMetadata:
    version: str
    block_id: int
    block_name: str
    release_tag: str
    status: str = "development"
    report_prefix: str = "ExcelBuilder_Run"
    updated_at: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def block_label(self) -> str:
        return f"Block{self.block_id}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectMetadata":
        version = str(data.get("version", "")).strip()
        block_id = int(data.get("block_id", 0))
        block_name = str(data.get("block_name", "")).strip()
        release_tag = str(data.get("release_tag", f"{version}-block{block_id}")).strip()
        status = str(data.get("status", "development")).strip() or "development"
        report_prefix = str(data.get("report_prefix", "ExcelBuilder_Run")).strip() or "ExcelBuilder_Run"
        updated_at = str(data.get("updated_at", "")).strip()
        notes = tuple(str(item) for item in data.get("notes", []) if str(item).strip())
        if not version:
            raise ValueError("version.json saknar version")
        if block_id <= 0:
            raise ValueError("version.json saknar giltigt block_id")
        if not block_name:
            raise ValueError("version.json saknar block_name")
        return cls(
            version=version,
            block_id=block_id,
            block_name=block_name,
            release_tag=release_tag,
            status=status,
            report_prefix=report_prefix,
            updated_at=updated_at,
            notes=notes,
        )


@dataclass(frozen=True)
class ReleaseChecklistItem:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ProjectMetadataReport:
    metadata: ProjectMetadata
    source_path: Path
    checklist: tuple[ReleaseChecklistItem, ...]

    @property
    def is_release_ready(self) -> bool:
        return all(item.passed for item in self.checklist)
