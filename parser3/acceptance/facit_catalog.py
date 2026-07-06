"""Compatibility wrapper. Official facit source is parser_facit.yaml."""

from __future__ import annotations

from parser3.acceptance.facit_yaml_loader import FacitYamlLoader


class FacitCatalog:
    def rows_by_section(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for expectation in FacitYamlLoader().load():
            if expectation.required_names:
                result[expectation.section] = expectation.required_names
        return result
