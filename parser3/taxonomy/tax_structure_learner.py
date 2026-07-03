"""Early tax structure learner.

This block only provides lightweight rules. Later blocks will add the full golden
master driven learner.
"""

from __future__ import annotations


class TaxStructureLearner:
    def infer_group(self, recent_text: list[str]) -> str:
        for text in reversed(recent_text[-5:]):
            lower = text.lower()
            if "tillägg för farligt avfall" in lower:
                return "Tillägg för farligt avfall"
            if "tillägg för el-avfall" in lower:
                return "Tillägg för el-avfall"
            if "hanteringsavgifter" in lower:
                return "Hanteringsavgifter"
            if "övriga avgifter" in lower:
                return "Övriga avgifter"
        return ""
