from pathlib import Path
import subprocess
import sys


def test_check_test_syntax_tool_exists():
    assert Path("tools/check_test_syntax.py").exists()


def test_check_test_syntax_tool_runs_successfully():
    result = subprocess.run(
        [sys.executable, "tools/check_test_syntax.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "All test files parsed successfully" in result.stdout


def test_build_excel_report_runs_syntax_check_before_pytest():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "check_test_syntax.py" in text
    assert "test_syntax_report.txt" in text
    assert text.index("check_test_syntax.py") < text.index("pytest")
