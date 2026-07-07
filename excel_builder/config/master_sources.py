"""Central reader for immutable master source configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass(frozen=True)
class ProtectedSheetRule:
    sheet_name: str
    protected_columns: str
    rule: str


@dataclass(frozen=True)
class MasterSources:
    master_version: str
    word_master: Path
    excel_master: Path
    immutable: bool = True
    protected_sheets: tuple[ProtectedSheetRule, ...] = field(default_factory=tuple)

    def resolve_from(self, project_root: str | Path = ".") -> "MasterSources":
        root = Path(project_root)
        return MasterSources(
            master_version=self.master_version,
            word_master=(root / self.word_master).resolve(),
            excel_master=(root / self.excel_master).resolve(),
            immutable=self.immutable,
            protected_sheets=self.protected_sheets,
        )


class MasterSourcesReader:
    DEFAULT_CONFIG_PATH = Path("config/master_sources.json")

    def read(self, path: str | Path | None = None) -> MasterSources:
        config_path = Path(path) if path else self.DEFAULT_CONFIG_PATH
        data = json.loads(config_path.read_text(encoding="utf-8"))
        protected = []
        for sheet_name, rule_data in (data.get("protected_sheets") or {}).items():
            protected.append(
                ProtectedSheetRule(
                    sheet_name=str(sheet_name),
                    protected_columns=str(rule_data.get("protected_columns", "") or ""),
                    rule=str(rule_data.get("rule", "") or ""),
                )
            )
        return MasterSources(
            master_version=str(data.get("master_version", "") or ""),
            word_master=Path(str(data.get("word_master", "") or "")),
            excel_master=Path(str(data.get("excel_master", "") or "")),
            immutable=bool(data.get("immutable", True)),
            protected_sheets=tuple(protected),
        )

    def read_resolved(self, path: str | Path | None = None, project_root: str | Path = ".") -> MasterSources:
        return self.read(path).resolve_from(project_root)


def get_master_sources(path: str | Path | None = None) -> MasterSources:
    return MasterSourcesReader().read(path)
