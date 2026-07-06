from pathlib import Path


def test_project_scripts_exist():
    assert Path("excel_builder_project_run.py").exists()
    assert Path("build_sorsele_project.bat").exists()
    assert Path("build_all_projects.bat").exists()


def test_project_configs_exist():
    assert Path("data/projects/Sorsele/project_config.json").exists()
    assert Path("data/projects/Mala/project_config.json").exists()
    assert Path("data/projects/Norsjo/project_config.json").exists()


def test_report_package_includes_primary_project_output():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")

    assert r"output\projects\Sorsele" in text
    assert "ArbetsExcel_Sorsele_byggd.xlsx" in text


def test_build_excel_report_runs_primary_sorsele_project():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")

    assert "excel_builder_project_run.py" in text
    assert r"data\projects\Sorsele\project_config.json" in text
    assert "sorsele_project_run_console.txt" in text


def test_all_projects_script_keeps_batch_option_for_mala_norsjo_sorsele():
    text = Path("build_all_projects.bat").read_text(encoding="utf-8")

    assert r"data\projects\Sorsele\project_config.json" in text
    assert r"data\projects\Mala\project_config.json" in text
    assert r"data\projects\Norsjo\project_config.json" in text


def test_standard_tax_reference_is_not_project_specific():
    text = Path("docs/ExcelBuilder_Block13_StandardTaxReferenceSheets.md").read_text(encoding="utf-8")

    assert "global kunskap" in text.lower()
    assert "kommununika" in text.lower()
