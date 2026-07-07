from pathlib import Path


def test_build_excel_report_is_full_pipeline_with_v1_spec():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")

    assert "check_v1_spec.py" in text
    assert "excel_builder_context_resolve.py" in text
    assert "excel_builder_tax_codes.py" in text
    assert "excel_builder_decide_semantic.py" in text
    assert "excel_builder_project_run.py" in text
    assert "zip_excel_report.ps1" in text


def test_zip_report_includes_full_pipeline_and_spec_outputs():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")

    assert "v1_spec_report.txt" in text
    assert "tax_decision_semantic_report.txt" in text
    assert "context_resolution_report.txt" in text
    assert "tax_code_intelligence_report.txt" in text
    assert "ArbetsExcel_Sorsele_byggd.xlsx" in text


def test_build_pipeline_order_spec_before_tests_and_reports():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")

    assert text.index("check_v1_spec.py") < text.index("pytest")
    assert text.index("excel_builder_context_resolve.py") < text.index("pytest")
