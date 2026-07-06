from pathlib import Path


def test_output_structure_tool_exists():
    assert Path("tools/organize_output.py").exists()


def test_build_report_mentions_word_output_folder():
    text = Path("build_report.bat").read_text(encoding="utf-8")
    assert "output\word" in text
    assert "docs-mappen" in text
