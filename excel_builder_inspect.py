from __future__ import annotations

import argparse

from excel_builder.io import WorkbookProfiler
from excel_builder.reports import WorkbookProfileReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect Arbets-Excel structure")
    parser.add_argument("--workbook", default="C:\\PyProjects\\data\\Master.xlsx")
    parser.add_argument("--out", default="output/excel/arbets_excel_profile_report.txt")
    args = parser.parse_args()

    profile = WorkbookProfiler().profile(args.workbook)
    report = WorkbookProfileReporter().write(profile, args.out)

    print("Arbets-Excel profile klar")
    print(f"Workbook: {args.workbook}")
    print(f"Sheets: {profile.sheet_count}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
