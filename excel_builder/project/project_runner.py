"""Run one isolated municipality project.

Important:
Project data is local and must never be mixed between municipalities.
Global rule knowledge may be reused, but Word/EDP/output files are project-local.
"""

from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime

from excel_builder.edp import EdpExportReader, IsolatedWorkbookBuilder
from excel_builder.models import ProjectConfig, ProjectRunResult
from excel_builder.reports import EdpRunReporter


class ProjectRunner:
    def run(self, config: ProjectConfig) -> ProjectRunResult:
        result = ProjectRunResult(config=config)
        output_dir = Path(config.output_dir)
        excel_dir = output_dir / "excel"
        reports_dir = output_dir / "reports"
        manifest_dir = output_dir / "manifest"

        excel_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)
        manifest_dir.mkdir(parents=True, exist_ok=True)

        if not config.municipality:
            result.warnings.append("Kommun saknas i projektkonfiguration.")
        if not Path(config.edp_export_path).exists():
            result.warnings.append(f"EDP-export saknas: {config.edp_export_path}")

        export = EdpExportReader().read(config.edp_export_path, config.municipality)
        result.warnings.extend(export.warnings)

        safe_name = self._safe_name(config.municipality)
        excel_path = excel_dir / f"ArbetsExcel_{safe_name}_byggd.xlsx"
        report_path = reports_dir / f"edp_isolated_run_report_{safe_name}.txt"
        manifest_path = manifest_dir / "project_run_manifest.json"

        IsolatedWorkbookBuilder().build(export, excel_path)
        EdpRunReporter().write(export, excel_path, report_path)

        manifest = {
            "created": datetime.now().isoformat(timespec="seconds"),
            "municipality": config.municipality,
            "word_path": config.word_path,
            "edp_export_path": config.edp_export_path,
            "parser_result_path": config.parser_result_path,
            "output_excel": str(excel_path),
            "output_report": str(report_path),
            "warnings": result.warnings,
            "isolation_rule": "Projektdata får inte blandas mellan kommuner. Generella regelverk får återanvändas.",
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        result.excel_path = str(excel_path)
        result.report_path = str(report_path)
        result.manifest_path = str(manifest_path)
        return result

    def _safe_name(self, value: str) -> str:
        return (
            str(value or "")
            .replace("å", "a").replace("ä", "a").replace("ö", "o")
            .replace("Å", "A").replace("Ä", "A").replace("Ö", "O")
            .replace(" ", "_")
        )
