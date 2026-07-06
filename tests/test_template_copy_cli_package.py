from pathlib import Path


def test_template_copy_cli_exists():
    assert Path("excel_builder_template_copy.py").exists()
    assert Path("build_template_copy.bat").exists()


def test_template_version_history_exists():
    assert Path("data/master_templates/VERSION_HISTORY.md").exists()


def test_docs_include_user_approval_rule():
    text = Path("docs/ExcelBuilder_Block19_TemplateMasterVersioning.md").read_text(encoding="utf-8")
    assert "fråga användaren först" in text.lower()
    assert "ny versionsbaserad master" in text.lower()
