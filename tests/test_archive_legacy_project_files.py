from pathlib import Path

from tools.archive_legacy_project_files import archive_legacy_project_files


def test_archive_legacy_project_files_moves_legacy_masters_and_keeps_v1(tmp_path):
    legacy = tmp_path / "data" / "master_templates" / "ArbetsExcel_Template_v0.9.4_draft.xlsx"
    current = tmp_path / "data" / "master_templates" / "ArbetsExcel_Template_v1.0.xlsx"
    legacy.parent.mkdir(parents=True)
    legacy.write_text("legacy", encoding="utf-8")
    current.write_text("current", encoding="utf-8")

    archive_legacy_project_files(tmp_path)

    assert not legacy.exists()
    assert current.exists()
    assert (tmp_path / "archive" / "legacy_project_files" / "data" / "master_templates" / legacy.name).exists()


def test_archive_legacy_project_files_keeps_docs_folders_with_readme(tmp_path):
    docs_install = tmp_path / "docs" / "install"
    docs_changelog = tmp_path / "docs" / "changelogg"
    docs_install.mkdir(parents=True)
    docs_changelog.mkdir(parents=True)
    (docs_install / "INSTALL_old.md").write_text("old", encoding="utf-8")
    (docs_changelog / "CHANGELOG_old.md").write_text("old", encoding="utf-8")

    archive_legacy_project_files(tmp_path)

    assert (docs_install / "README.md").exists()
    assert (docs_changelog / "README.md").exists()
    assert (tmp_path / "archive" / "legacy_project_files" / "docs" / "install" / "INSTALL_old.md").exists()
    assert (tmp_path / "archive" / "legacy_project_files" / "docs" / "changelogg" / "CHANGELOG_old.md").exists()
