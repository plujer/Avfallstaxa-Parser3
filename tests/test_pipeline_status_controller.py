from pathlib import Path
import json

from tools.pipeline_status import write_status


def test_pipeline_status_success_allows_commit(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    diag = Path("output/diagnostics")
    diag.mkdir(parents=True)
    (diag / "pytest_report.txt").write_text("================ 352 passed, 3 warnings ================", encoding="utf-8")

    code = write_status("Block49 Pipeline Controller", pipeline_failed=False, warnings_failed=False, pytest_failed=False)

    data = json.loads((diag / "pipeline_status.json").read_text(encoding="utf-8"))
    assert code == 0
    assert data["overall_status"] == "SUCCESS"
    assert data["commit_allowed"] is True
    assert data["tests"]["passed"] == 352
    assert data["tests"]["failed"] == 0


def test_pipeline_status_warning_blocks_commit_but_not_run(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    diag = Path("output/diagnostics")
    diag.mkdir(parents=True)
    (diag / "pytest_report.txt").write_text("352 passed", encoding="utf-8")

    code = write_status("Block49 Pipeline Controller", pipeline_failed=False, warnings_failed=True, pytest_failed=False)

    data = json.loads((diag / "pipeline_status.json").read_text(encoding="utf-8"))
    assert code == 0
    assert data["overall_status"] == "WARNING"
    assert data["commit_allowed"] is False


def test_pipeline_status_failed_tests_blocks_commit(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    diag = Path("output/diagnostics")
    diag.mkdir(parents=True)
    (diag / "pytest_report.txt").write_text("4 failed, 340 passed", encoding="utf-8")

    code = write_status("Block49 Pipeline Controller", pipeline_failed=False, warnings_failed=False, pytest_failed=True)

    data = json.loads((diag / "pipeline_status.json").read_text(encoding="utf-8"))
    assert code == 1
    assert data["overall_status"] == "FAILED"
    assert data["commit_allowed"] is False
