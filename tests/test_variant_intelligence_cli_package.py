from pathlib import Path


def test_variant_intelligence_cli_exists():
    assert Path("excel_builder_variant_intelligence.py").exists()


def test_build_excel_report_runs_variant_intelligence():
    content = Path("build_excel_report.bat").read_text(encoding="utf-8", errors="ignore")
    assert "excel_builder_variant_intelligence.py" in content


def test_zip_includes_variant_intelligence_reports():
    content = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8", errors="ignore")
    assert "variant_intelligence_report.txt" in content
    assert "variant_profiles.csv" in content
