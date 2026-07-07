from __future__ import annotations
import argparse
from excel_builder.schema import WorkbookSchemaScanner
from excel_builder.reports.workbook_schema_reporter import WorkbookSchemaReporter

def main() -> None:
    parser = argparse.ArgumentParser(description="Scan workbook schema")
    parser.add_argument("--workbook", default="data/master_templates/ArbetsExcel_Template_v1.0.xlsx")
    parser.add_argument("--txt", default="output/excel/workbook_schema_report.txt")
    parser.add_argument("--sheets-csv", default="output/excel/workbook_schema_sheets.csv")
    parser.add_argument("--headers-csv", default="output/excel/workbook_schema_header_candidates.csv")
    args = parser.parse_args()

    schema = WorkbookSchemaScanner().scan(args.workbook)
    reporter = WorkbookSchemaReporter()
    txt = reporter.write_txt(schema, args.txt)
    sheets_csv = reporter.write_sheets_csv(schema, args.sheets_csv)
    headers_csv = reporter.write_headers_csv(schema, args.headers_csv)

    print("Workbook Schema Scan klar")
    print(f"Workbook: {args.workbook}")
    print(f"Sheets: {schema.sheet_count}")
    print(f"Defined names: {len(schema.defined_names)}")
    print(f"Warnings: {len(schema.warnings)}")
    print(f"TXT: {txt}")
    print(f"Sheets CSV: {sheets_csv}")
    print(f"Headers CSV: {headers_csv}")

if __name__ == "__main__":
    main()
