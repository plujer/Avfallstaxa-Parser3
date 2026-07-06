"""Validate that documented EDP rules are present before matching changes."""

from __future__ import annotations

from excel_builder.models import Rulebook


class EdpRuleValidator:
    REQUIRED_RULES = [
        "Taxakod",
        "strTaxekod",
        "strTaxebenamning",
        "strTaxedelAvser",
        "strFaktor",
        "strFormel",
        "Aktuellt pris",
        "Taxa_från_edp",
        "Taxa_Saknas",
        "får aldrig redigeras manuellt",
    ]

    def validate(self, rulebook: Rulebook) -> list[str]:
        warnings: list[str] = []
        for rule in self.REQUIRED_RULES:
            if not rulebook.contains_text(rule):
                warnings.append(f"Saknar dokumenterad regel/term: {rule}")
        return warnings
