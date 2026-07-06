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
    assert "output\projects\Sorsele" in text
    assert "output\projects\Mala" in text
    assert "output\projects\Norsjo" in text
