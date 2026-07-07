from pathlib import Path
import subprocess
import sys


def test_v1_specification_files_exist():
    assert Path("docs/spec/ExcelBuilder_v1_0_Specification.md").exists()
    assert Path("docs/spec/ExcelBuilder_v1_0_Roadmap.md").exists()
    assert Path("docs/spec/ExcelBuilder_v1_0_Invariants.md").exists()


def test_v1_specification_contains_core_invariants():
    text = Path("docs/spec/ExcelBuilder_v1_0_Specification.md").read_text(encoding="utf-8")
    assert "Kommunens EDP är facit" in text
    assert "Taxa_från_edp" in text
    assert "NOT_A_TAXA" in text
    assert "Masterarbetsboken" in text


def test_v1_spec_validation_tool_runs():
    result = subprocess.run(
        [sys.executable, "tools/check_v1_spec.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "validation passed" in result.stdout
