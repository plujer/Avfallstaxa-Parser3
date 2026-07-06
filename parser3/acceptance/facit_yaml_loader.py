"""Load parser facit from YAML."""

from __future__ import annotations

from pathlib import Path
import yaml

from parser3.acceptance.acceptance_models import AcceptanceExpectation


class FacitYamlLoader:
    def load(self, path: str | Path = "parser_facit.yaml") -> list[AcceptanceExpectation]:
        facit_path = Path(path)
        if not facit_path.exists():
            facit_path = Path("golden_master/parser_facit.yaml")

        data = yaml.safe_load(facit_path.read_text(encoding="utf-8")) or {}
        sections = data.get("sections", {})
        expectations: list[AcceptanceExpectation] = []

        for section, payload in sections.items():
            tax_rows = payload.get("tax_rows") or []
            ignored_rows = payload.get("ignored_rows") or []
            expected_count = int(payload.get("tax_count") or len(tax_rows))

            required_names = [
                str(row.get("taxapunkt", "")).strip()
                for row in tax_rows
                if isinstance(row, dict) and str(row.get("taxapunkt", "")).strip()
            ]
            ignored_names = [
                str(row.get("taxapunkt", "")).strip()
                for row in ignored_rows
                if isinstance(row, dict) and str(row.get("taxapunkt", "")).strip()
            ]

            expectations.append(
                AcceptanceExpectation(
                    section=str(section),
                    expected_count=expected_count,
                    required_names=required_names,
                    ignored_names=ignored_names,
                )
            )
        return expectations
