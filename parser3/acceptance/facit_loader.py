"""Load manually verified facit expectations."""

from __future__ import annotations

from parser3.acceptance.acceptance_models import AcceptanceExpectation
from parser3.acceptance.facit_catalog import FacitCatalog


class FacitLoader:
    def load_builtin(self) -> list[AcceptanceExpectation]:
        catalog = FacitCatalog().rows_by_section()
        return [
            AcceptanceExpectation(section="6.1.1", expected_count=6),
            AcceptanceExpectation(
                section="6.1.2",
                expected_count=103,
                ignored_names=[
                    "Toner, färgpatron utan elektronik",
                    "Toner, färgpatron utan elektronik – se farligt avfall",
                    "Toner, färgpatron utan elektronik - se farligt avfall",
                ],
                required_names=catalog.get("6.1.2", []),
            ),
            AcceptanceExpectation(section="6.1.3", expected_count=4),
            AcceptanceExpectation(section="6.1.4", expected_count=4),
        ]
