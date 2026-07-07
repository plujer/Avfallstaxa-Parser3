from __future__ import annotations

from pathlib import Path

from excel_builder.models.project_metadata_models import ProjectMetadataReport


class ProjectMetadataReporter:
    def write(self, report: ProjectMetadataReport, out_path: str | Path) -> Path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        metadata = report.metadata
        lines = [
            "Excel Builder Project Metadata Report",
            "",
            f"Version: {metadata.version}",
            f"Block: {metadata.block_id}",
            f"Block name: {metadata.block_name}",
            f"Release tag: {metadata.release_tag}",
            f"Status: {metadata.status}",
            f"Report prefix: {metadata.report_prefix}",
            f"Metadata source: {report.source_path}",
            "",
            "Release checklist:",
        ]
        for item in report.checklist:
            marker = "OK" if item.passed else "MISSING"
            lines.append(f"- [{marker}] {item.name}: {item.detail}")
        if metadata.notes:
            lines += ["", "Notes:"]
            lines += [f"- {note}" for note in metadata.notes]
        lines += ["", f"Release ready: {report.is_release_ready}"]
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return out
