"""Build a tax code parse catalog from standard taxes and rule repository."""

from __future__ import annotations

from excel_builder.models import RuleRepository, StandardTaxCatalog, TaxCodeParseReport
from excel_builder.taxcode.tax_code_parser import TaxCodeParser


class TaxCodeCatalogBuilder:
    def __init__(self) -> None:
        self.parser = TaxCodeParser()

    def from_standard_and_rules(self, catalog: StandardTaxCatalog, repo: RuleRepository) -> TaxCodeParseReport:
        codes: set[str] = set()

        for row in catalog.rows:
            if row.strTaxekod:
                codes.add(row.strTaxekod)

        for rule in repo.rules:
            if rule.tax_code:
                codes.add(rule.tax_code)
            if rule.standard_tax_code:
                codes.add(rule.standard_tax_code)

        report = TaxCodeParseReport()
        for code in sorted(codes):
            report.parsed_codes.append(self.parser.parse(code))

        return report
