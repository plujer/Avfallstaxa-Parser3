from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

DIAG = Path("output/diagnostics")
STATUS_JSON = DIAG / "pipeline_status.json"
STATUS_TXT = DIAG / "pipeline_status.txt"
PYTEST_REPORT = DIAG / "pytest_report.txt"
LATEST_STATUS = DIAG / "latest_run_status.txt"


def parse_pytest_report() -> tuple[int | None, int, str]:
    if not PYTEST_REPORT.exists():
        return None, 0, "UNKNOWN"
    text = PYTEST_REPORT.read_text(encoding="utf-8", errors="replace")
    passed_matches = re.findall(r"(\d+)\s+passed", text, flags=re.IGNORECASE)
    failed_matches = re.findall(r"(\d+)\s+failed", text, flags=re.IGNORECASE)
    passed = int(passed_matches[-1]) if passed_matches else None
    failed = int(failed_matches[-1]) if failed_matches else 0
    if failed:
        return passed, failed, "FAILED"
    if passed is not None:
        return passed, 0, "OK"
    return None, 0, "UNKNOWN"


def bool_arg(value: str | int | bool) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "failed", "error"}


def write_status(block_name: str, pipeline_failed: bool, warnings_failed: bool, pytest_failed: bool) -> int:
    DIAG.mkdir(parents=True, exist_ok=True)
    passed, failed, pytest_state = parse_pytest_report()

    # Explicit batch flags are authoritative for critical command failures.
    tests_ok = (not pytest_failed) and pytest_state == "OK" and failed == 0 and passed is not None
    critical_ok = not pipeline_failed

    if not critical_ok or not tests_ok:
        overall = "FAILED"
        commit_allowed = False
    elif warnings_failed:
        overall = "WARNING"
        commit_allowed = False
    else:
        overall = "SUCCESS"
        commit_allowed = True

    data = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "block_name": block_name,
        "overall_status": overall,
        "commit_allowed": commit_allowed,
        "critical_pipeline_failed": pipeline_failed,
        "warnings_failed": warnings_failed,
        "pytest_failed": pytest_failed,
        "tests": {
            "status": pytest_state,
            "passed": passed,
            "failed": failed,
        },
        "files": {
            "pytest_report": str(PYTEST_REPORT),
            "latest_run_status": str(LATEST_STATUS),
        },
    }
    STATUS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "Excel Builder Pipeline Status",
        f"Block: {block_name}",
        f"Overall: {overall}",
        f"Commit allowed: {'YES' if commit_allowed else 'NO'}",
        "",
        f"Critical pipeline failed: {'YES' if pipeline_failed else 'NO'}",
        f"Warnings: {'YES' if warnings_failed else 'NO'}",
        f"Tests: {pytest_state}",
        f"Passed: {passed if passed is not None else 'unknown'}",
        f"Failed: {failed}",
        "",
    ]
    if overall == "SUCCESS":
        lines.extend([
            "Next step:",
            "- Skicka senaste ZIP-filen från rapportzip\\ till ChatGPT.",
            "- Kör git_commit_block.bat först efter ChatGPT har godkänt körningen.",
        ])
    elif overall == "WARNING":
        lines.extend([
            "Next step:",
            "- Skicka senaste ZIP-filen från rapportzip\\ till ChatGPT för granskning.",
            "- Kör INTE git_commit_block.bat innan varningarna är godkända eller åtgärdade.",
        ])
    else:
        lines.extend([
            "Next step:",
            "- Kör INTE git_commit_block.bat.",
            "- Skicka rapportzip eller felrapport för felsökning.",
        ])
    STATUS_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if overall in {"SUCCESS", "WARNING"} else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block-name", required=True)
    parser.add_argument("--pipeline-failed", default="0")
    parser.add_argument("--warnings-failed", default="0")
    parser.add_argument("--pytest-failed", default="0")
    args = parser.parse_args()
    return write_status(
        block_name=args.block_name,
        pipeline_failed=bool_arg(args.pipeline_failed),
        warnings_failed=bool_arg(args.warnings_failed),
        pytest_failed=bool_arg(args.pytest_failed),
    )


if __name__ == "__main__":
    raise SystemExit(main())
