from __future__ import annotations

import argparse

from excel_builder.reports import TaxCodeReporter
from excel_builder.rules import MasterRuleRepositoryReader
from excel_builder.standard import StandardTaxReader
from excel_builder.taxcode import TaxCodeCatalogBuilder


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse and report EDP tax codes")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--workbook", default="data/ArbetsExcel_Reference.xlsx")
    parser.add_argument("--txt", default="output/excel/tax_code_intelligence_report.txt")
    parser.add_argument("--csv", default="output/excel/tax_code_intelligence.csv")
    args = parser.parse_args()

    catalog = StandardTaxReader().read(args.standard_tax)
    repo = MasterRuleRepositoryReader().read(args.workbook)

    report = TaxCodeCatalogBuilder().from_standard_and_rules(catalog, repo)

    txt = TaxCodeReporter().write_txt(report, args.txt)
    csv = TaxCodeReporter().write_csv(report, args.csv)

    print("Tax Code Intelligence klar")
    print(f"Tax codes: {report.total}")
    print(f"With family key: {report.parsed_with_family}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
