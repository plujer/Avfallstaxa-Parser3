import json
from pathlib import Path

from excel_builder.models.project_metadata_models import ProjectMetadataReport
from excel_builder.project_metadata import ProjectMetadataReader, ProjectMetadataReporter, ReleaseChecklistBuilder


def test_project_metadata_reader_reads_version_file(tmp_path):
    path = tmp_path / "version.json"
    path.write_text(json.dumps({
        "version": "v0.9.4",
        "block_id": 42,
        "block_name": "Project Metadata and Release Checklist",
        "release_tag": "v0.9.4-block42",
    }), encoding="utf-8")

    metadata = ProjectMetadataReader().read(path)

    assert metadata.version == "v0.9.4"
    assert metadata.block_id == 42
    assert metadata.block_label == "Block42"
    assert metadata.release_tag == "v0.9.4-block42"


def test_release_checklist_checks_standard_bat_files(tmp_path):
    for name in [
        "run_project.bat", "run_tests.bat", "run_reports.bat", "run_clean.bat",
        "git_commit_block.bat", "git_release_block.bat",
    ]:
        (tmp_path / name).write_text("@echo off\n", encoding="utf-8")
    (tmp_path / "docs" / "history").mkdir(parents=True)
    (tmp_path / "docs" / "PROJECT_STATUS.md").write_text("status", encoding="utf-8")
    (tmp_path / "docs" / "CHANGELOG.md").write_text("changelog", encoding="utf-8")
    (tmp_path / "docs" / "history" / "BLOCK_HISTORY.md").write_text("history", encoding="utf-8")

    metadata = ProjectMetadataReader().read(Path("version.json"))
    checklist = ReleaseChecklistBuilder().build(metadata, tmp_path)

    assert all(item.passed for item in checklist)


def test_project_metadata_reporter_writes_report(tmp_path):
    metadata = ProjectMetadataReader().read(Path("version.json"))
    checklist = ReleaseChecklistBuilder().build(metadata, ".")
    report = ProjectMetadataReport(metadata=metadata, source_path=Path("version.json"), checklist=checklist)
    out = ProjectMetadataReporter().write(report, tmp_path / "project_metadata_report.txt")

    text = out.read_text(encoding="utf-8")
    assert "Excel Builder Project Metadata Report" in text
    assert "Version: v0.9.4" in text
    assert "Block: 42" in text
    assert "Release checklist:" in text
