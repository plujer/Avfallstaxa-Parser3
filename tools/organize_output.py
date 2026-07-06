"""Deprecated.

Reports are now written directly to output subfolders by build_report.bat and
parser.py. This file remains as a harmless compatibility stub in case an old
command calls it.
"""

from __future__ import annotations


def main() -> None:
    print("organize_output.py is deprecated; no action needed.")


if __name__ == "__main__":
    main()
