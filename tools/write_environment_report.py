"""Write a small environment report for debugging."""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return (completed.stdout or completed.stderr or "").strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def main() -> None:
    print("Parser 3.1 environment report")
    print()
    print(f"cwd: {Path.cwd()}")
    print(f"python: {sys.executable}")
    print(f"python_version: {sys.version}")
    print(f"platform: {platform.platform()}")
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', '')}")
    print()
    print("git status:")
    print(run(["git", "status", "--short"]))
    print()
    print("git branch:")
    print(run(["git", "branch", "--show-current"]))
    print()
    print("pip freeze:")
    print(run([sys.executable, "-m", "pip", "freeze"]))


if __name__ == "__main__":
    main()
