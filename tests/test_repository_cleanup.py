from pathlib import Path
import importlib.util


def load_cleanup_module():
    path = Path("tools/cleanup_duplicate_tests.py")
    spec = importlib.util.spec_from_file_location("cleanup_duplicate_tests", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cleanup_duplicate_tests_tool_exists():
    assert Path("tools/cleanup_duplicate_tests.py").exists()


def test_find_duplicate_test_filenames_detects_duplicates(tmp_path):
    module = load_cleanup_module()

    root = tmp_path / "tests"
    (root / "tests").mkdir(parents=True)
    (root / "test_a.py").write_text("", encoding="utf-8")
    (root / "tests" / "test_a.py").write_text("", encoding="utf-8")

    duplicates = module.find_duplicate_test_filenames(root)

    assert "test_a.py" in duplicates
    assert len(duplicates["test_a.py"]) == 2


def test_build_excel_report_runs_cleanup_before_pytest():
    text = Path("build_excel_report.bat").read_text(encoding="utf-8")
    assert "cleanup_duplicate_tests.py" in text
    assert "test_cleanup_report.txt" in text
    assert text.index("cleanup_duplicate_tests.py") < text.index("pytest")
