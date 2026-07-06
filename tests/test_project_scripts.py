from pathlib import Path


def test_project_scripts_exist():
    assert Path("excel_builder_project_run.py").exists()
    assert Path("build_sorsele_project.bat").exists()
    assert Path("build_all_projects.bat").exists()


def test_project_configs_exist():
    assert Path("data/projects/Sorsele/project_config.json").exists()
    assert Path("data/projects/Mala/project_config.json").exists()
    assert Path("data/projects/Norsjo/project_config.json").exists()


def test_report_package_includes_project_outputs():
    text = Path("tools/zip_excel_report.ps1").read_text(encoding="utf-8")

    assert r"output\projects\Sorsele" in text
    assert r"output\projects\Mala" in text
    assert r"output\projects\Norsjo" in text


def test_build_excel_report_runs_project_outputs():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")

    assert "excel_builder_project_run.py" in text
    assert r"data\projects\Sorsele\project_config.json" in text
    assert r"data\projects\Mala\project_config.json" in text
    assert r"data\projects\Norsjo\project_config.json" in text


def test_standard_tax_reference_is_not_project_specific():
    text = Path("docs/ExcelBuilder_Block13_StandardTaxReferenceSheets.md").read_text(encoding="utf-8")

    assert "global kunskap" in text.lower()
    assert "kommununika" in text.lower()
