"""Load facit expectations from parser_facit.yaml."""

from __future__ import annotations

from parser3.acceptance.acceptance_models import AcceptanceExpectation
from parser3.acceptance.facit_yaml_loader import FacitYamlLoader


class FacitLoader:
    def load_builtin(self) -> list[AcceptanceExpectation]:
        return FacitYamlLoader().load()
