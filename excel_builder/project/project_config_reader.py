"""Read an isolated project config."""

from __future__ import annotations

from pathlib import Path
import json

from excel_builder.models import ProjectConfig


class ProjectConfigReader:
    def read(self, path: str | Path) -> ProjectConfig:
        source = Path(path)
        data = json.loads(source.read_text(encoding="utf-8"))

        return ProjectConfig(
            municipality=str(data.get("municipality", "") or ""),
            word_path=str(data.get("word_path", "") or ""),
            edp_export_path=str(data.get("edp_export_path", "") or ""),
            output_dir=str(data.get("output_dir", "") or ""),
            parser_result_path=str(data.get("parser_result_path", "output/reports/parser3_result.json") or ""),
            notes=str(data.get("notes", "") or ""),
        )
