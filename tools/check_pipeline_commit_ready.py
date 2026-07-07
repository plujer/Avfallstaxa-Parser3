from __future__ import annotations

import json
from pathlib import Path

STATUS_JSON = Path("output/diagnostics/pipeline_status.json")


def main() -> int:
    if not STATUS_JSON.exists():
        print("pipeline_status.json saknas. Kör run_project.bat först.")
        return 1
    data = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    overall = data.get("overall_status", "UNKNOWN")
    commit_allowed = bool(data.get("commit_allowed"))
    tests = data.get("tests", {})
    print("Senaste pipeline-status")
    print(f"Overall: {overall}")
    print(f"Tests: {tests.get('status', 'UNKNOWN')}")
    print(f"Passed: {tests.get('passed', 'unknown')}")
    print(f"Failed: {tests.get('failed', 'unknown')}")
    print(f"Commit allowed: {'YES' if commit_allowed else 'NO'}")
    if not commit_allowed:
        print("Commit stoppad. Kör run_project.bat och skicka rapportzip för granskning.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
