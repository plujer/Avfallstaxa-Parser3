from __future__ import annotations

import argparse

from excel_builder.io import ParserMatchReader
from excel_builder.knowledge import TaxKnowledgeExtractor, KnowledgeIndexBuilder
from excel_builder.standard import StandardTaxReader
from excel_builder.reports import KnowledgeIndexReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Knowledge Index")
    parser.add_argument("--parser-result", default="output/reports/parser3_result.json")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--txt", default="output/excel/knowledge_index_report.txt")
    parser.add_argument("--csv", default="output/excel/knowledge_index.csv")
    args = parser.parse_args()

    parser_rows = ParserMatchReader().read(args.parser_result)
    knowledge_report = TaxKnowledgeExtractor().extract(parser_rows)
    catalog = StandardTaxReader().read(args.standard_tax)
    index = KnowledgeIndexBuilder().build(knowledge_report, catalog)

    txt = KnowledgeIndexReporter().write_txt(index, args.txt)
    csv = KnowledgeIndexReporter().write_csv(index, args.csv)

    print("Knowledge Index klar")
    print(f"Parser rows: {len(parser_rows)}")
    print(f"Index entries: {index.entry_count}")
    print(f"Standard rows indexed: {index.standard_row_count}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")


if __name__ == "__main__":
    main()
