"""Parse tax codes into stable family keys."""

from __future__ import annotations

from excel_builder.models import TaxFamilyKey, TaxFamilyMember
from excel_builder.taxcode.tax_code_parser import TaxCodeParser


class TaxFamilyParser:
    """Converts tax codes to family members using the conservative tax code parser."""

    def __init__(self) -> None:
        self.tax_code_parser = TaxCodeParser()

    def parse_member(self, tax_code: str, source: str = "") -> TaxFamilyMember:
        parsed = self.tax_code_parser.parse(tax_code)
        key = TaxFamilyKey(
            prefix=parsed.prefix,
            volume_liter=parsed.volume_liter,
            waste_code=parsed.waste_code,
        )
        return TaxFamilyMember(
            tax_code=parsed.original_code,
            family_key=key,
            interval=parsed.interval,
            variant=parsed.variant,
            source=source,
            parsed=parsed,
        )

    def family_code(self, tax_code: str) -> str:
        return self.parse_member(tax_code).family_key.value
