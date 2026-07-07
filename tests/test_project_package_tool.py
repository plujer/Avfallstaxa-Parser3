from pathlib import Path


def test_project_package_tool_outputs_to_project_packages_folder():
    text = Path("tools/create_project_package.py").read_text(encoding="utf-8")

    assert 'root / "project_packages"' in text
    assert 'project_packages/Project_For_ChatGPT.zip' in text
    assert '"project_packages"' in text


def test_run_project_creates_project_package_after_reports():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")

    assert "create_project_package.py" in text
    assert text.index("zip_excel_report.ps1") < text.index("create_project_package.py")
    assert "project_packages\\Project_For_ChatGPT.zip" in text or "project_packages/Project_For_ChatGPT.zip" in text
