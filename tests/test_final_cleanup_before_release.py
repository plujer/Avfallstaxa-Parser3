from pathlib import Path


def test_zip_output_does_not_include_archive_folder_as_source():
    text = Path("tools/zip_output.ps1").read_text(encoding="utf-8")
    assert '"output\archive"' not in text
    assert "$paths = @(" in text
    assert "output\acceptance" in text
    assert "output\word" in text


def test_build_report_keeps_rapportzip_output():
    text = Path("build_report.bat").read_text(encoding="utf-8")
    assert "rapportzip" in text
    assert "output\diagnostics\pytest_report.txt" in text


def test_release_ready_docs_folders_exist():
    assert Path("docs/install").exists()
    assert Path("docs/changelogg").exists()
