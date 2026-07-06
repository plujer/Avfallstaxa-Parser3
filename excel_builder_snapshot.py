from __future__ import annotations

import argparse

from excel_builder.io import WorkbookSnapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Arbets-Excel snapshot")
    parser.add_argument("--workbook", default="C:\\PyProjects\\data\\Master.xlsx")
    parser.add_argument("--out", default="output/excel/arbets_excel_snapshot.txt")
    parser.add_argument("--max-rows", type=int, default=40)
    args = parser.parse_args()

    out = WorkbookSnapshot().write_snapshot(args.workbook, args.out, args.max_rows)
    print("Arbets-Excel snapshot klar")
    print(f"Snapshot: {out}")


if __name__ == "__main__":
    main()
