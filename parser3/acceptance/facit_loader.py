"""Load manually verified facit expectations.

The built-in expectations are only the sections we have explicitly verified in
conversation. More sections should be added only after manual approval.
"""

from __future__ import annotations

from parser3.acceptance.acceptance_models import AcceptanceExpectation


class FacitLoader:
    def load_builtin(self) -> list[AcceptanceExpectation]:
        return [
            AcceptanceExpectation(
                section="6.1.1",
                expected_count=6,
            ),
            AcceptanceExpectation(
                section="6.1.2",
                expected_count=103,
                ignored_names=[
                    "Toner, färgpatron utan elektronik",
                    "Toner, färgpatron utan elektronik – se farligt avfall",
                    "Toner, färgpatron utan elektronik - se farligt avfall",
                ],
                required_names=[
                    "Asbest, emballerat",
                    "Smittförande avfall",
                    "Rökdetektor med Am 241",
                ],
            ),
            AcceptanceExpectation(
                section="6.1.3",
                expected_count=4,
            ),
            AcceptanceExpectation(
                section="6.1.4",
                expected_count=4,
            ),
        ]
