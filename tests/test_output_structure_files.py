from pathlib import Path


def test_output_structure_tool_exists():
    # Kept as compatibility stub after output reports started writing directly
    # to subfolders.
    assert Path("tools/organize_output.py").exists()


def test_build_report_mentions_word_output_folder():
    text = Path("build_report.bat").read_text(encoding="utf-8")
    assert "output\word" in text
    assert "rapportzip" in text
    assert "docs-mappen" not in text


def test_build_report_uses_rapportzip_not_docs_for_feedback_zip():
    text = Path("build_report.bat").read_text(encoding="utf-8")
    assert "rapportzip-mappen" in text
    assert "Skapar zip i rapportzip" in text


def test_build_report_writes_directly_to_diagnostics():
    text = Path("build_report.bat").read_text(encoding="utf-8")
    assert "output\diagnostics\parser_console.txt" in text
    assert "output\diagnostics\pytest_report.txt" in text
