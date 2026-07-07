from __future__ import annotations

import os
import re
import time
from pathlib import Path

REPORT = Path("output/diagnostics/pytest_report.txt")
STATUS = Path("output/diagnostics/latest_run_status.txt")


def parse_report(text: str) -> tuple[int | None, int | None, str]:
    """Parse pytest summary text.

    Handles examples such as:
    - "344 passed"
    - "10 failed, 334 passed"
    - "4 failed, 340 passed, 3 warnings"
    """
    failed = 0
    passed = None

    m_failed = re.search(r"(\d+)\s+failed", text, flags=re.IGNORECASE)
    if m_failed:
        failed = int(m_failed.group(1))

    m_passed = re.search(r"(\d+)\s+passed", text, flags=re.IGNORECASE)
    if m_passed:
        passed = int(m_passed.group(1))

    if failed:
        return passed, failed, "FAILED"
    if passed is not None:
        return passed, 0, "OK"
    return None, None, "UNKNOWN"


def write_status_safely(message: str) -> None:
    """Write status without colliding with BAT redirection or locked files.

    Previous versions wrote directly to latest_run_status.txt while
    git_commit_block.bat also redirected Python output to the same file. On
    Windows this can lock the file and raise PermissionError.

    This function writes to a temporary file first and then atomically replaces
    the status file. If the file is temporarily locked, it retries briefly.
    """
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATUS.with_suffix(STATUS.suffix + ".tmp")
    data = message + "\n"

    for attempt in range(8):
        try:
            tmp.write_text(data, encoding="utf-8")
            os.replace(tmp, STATUS)
            return
        except PermissionError:
            time.sleep(0.25 * (attempt + 1))

    # Last attempt: do not crash commit check just because the diagnostics file
    # is locked. The console output still contains the authoritative status.
    try:
        fallback = STATUS.with_name("latest_run_status_fallback.txt")
        fallback.write_text(data, encoding="utf-8")
    except PermissionError:
        pass


def main() -> int:
    if not REPORT.exists():
        message = "Tests: UNKNOWN\npytest_report.txt saknas. Kor run_project.bat."
        print(message)
        write_status_safely(message)
        return 1

    text = REPORT.read_text(encoding="utf-8", errors="replace")
    passed, failed, state = parse_report(text)

    if state == "OK":
        message = f"Tests: OK\nPassed: {passed}\nFailed: 0"
        code = 0
    elif state == "FAILED":
        message = f"Tests: FAILED\nPassed: {passed if passed is not None else 'unknown'}\nFailed: {failed}"
        code = 1
    else:
        message = "Tests: UNKNOWN\nKunde inte lasa testresultat fran pytest_report.txt."
        code = 1

    print(message)
    write_status_safely(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
