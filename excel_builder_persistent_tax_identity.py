from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.persistent_identity import PersistentTaxIdentityEngine
from excel_builder.reports.persistent_tax_identity_reporter import PersistentTaxIdentityReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Build persistent tax identity report")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--txt", default="output/excel/persistent_tax_identity_report.txt")
    parser.add_argument("--csv", default="output/excel/persistent_tax_identity.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    report = PersistentTaxIdentityEngine().build(parser_rows)

    txt = PersistentTaxIdentityReporter().write_txt(report, args.txt)
    csv = PersistentTaxIdentityReporter().write_csv(report, args.csv)

    print("Persistent Tax Identity klar")
    print(f"Rows: {len(parser_rows)}")
    print(f"Identities: {report.total}")
    print(f"Duplicate content groups: {report.duplicate_content_groups}")
    print(f"Warnings: {len(report.warnings)}")
    print(f"Passed: {report.passed}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
