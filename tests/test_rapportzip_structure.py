from pathlib import Path


def test_zip_output_targets_rapportzip():
    text = Path("tools/zip_output.ps1").read_text(encoding="utf-8")
    assert "$zipDir = "rapportzip"" in text


def test_build_report_mentions_rapportzip():
    text = Path("build_report.bat").read_text(encoding="utf-8")
    assert "rapportzip" in text
