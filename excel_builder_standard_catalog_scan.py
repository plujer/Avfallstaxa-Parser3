from __future__ import annotations

import argparse

from excel_builder.standard import StandardCatalogSchemaScanner, StandardTaxReader, StandardCatalogNormalizer
from excel_builder.reports import StandardCatalogSchemaReporter


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan and normalize standard tax catalog")
    parser.add_argument("--standard-tax", default="data/edp_standard/EDP_Future_Standard_Taxor_Renhallning.xlsx")
    parser.add_argument("--txt", default="output/excel/standard_catalog_schema_report.txt")
    parser.add_argument("--csv", default="output/excel/standard_catalog_schema.csv")
    parser.add_argument("--normalized", default="output/excel/EDP_Standardtaxor_normalized.xlsx")
    args = parser.parse_args()

    schema = StandardCatalogSchemaScanner().scan(args.standard_tax)
    txt = StandardCatalogSchemaReporter().write_txt(schema, args.txt)
    csv = StandardCatalogSchemaReporter().write_csv(schema, args.csv)

    catalog = StandardTaxReader().read(args.standard_tax)
    normalized = StandardCatalogNormalizer().write(catalog, args.normalized)

    print("Standard Catalog Scan klar")
    print(f"Source: {args.standard_tax}")
    print(f"Sheets: {schema.sheet_count}")
    print(f"Sections: {schema.section_count}")
    print(f"Estimated standard rows: {schema.estimated_standard_rows}")
    print(f"Read standard rows: {catalog.row_count}")
    print(f"TXT: {txt}")
    print(f"CSV: {csv}")
    print(f"Normalized: {normalized}")


if __name__ == "__main__":
    main()
