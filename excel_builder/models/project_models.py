"""Project models for isolated Excel Builder runs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProjectConfig:
    municipality: str
    word_path: str
    edp_export_path: str
    output_dir: str
    parser_result_path: str = "output/reports/parser3_result.json"
    notes: str = ""


@dataclass
class ProjectRunResult:
    config: ProjectConfig
    excel_path: str = ""
    report_path: str = ""
    manifest_path: str = ""
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.warnings) == 0
