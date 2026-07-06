"""Name normalization for acceptance comparison.

This layer is only for comparing parser output with facit. It must not change the
source Word text or the generated Excel rows.
"""

from __future__ import annotations

import re


class NameNormalizer:
    ALIASES = {
        "förpackningar, tömde ej rengjorda": "förpackningar, tömda ej rengjorda",
        "gasol inkl tub": "gasol inkl. tub",
        "flourvätesyra": "fluorvätesyra",
        "surt oorganisk fast ämne": "surt oorganiskt fast ämne",
        "surt organisk fast ämne": "surt organiskt fast ämne",
        "rengöring/vaskmedel fast": "rengörings-/vaskmedel fast",
        "färg-,lack-, limburkar vattenbaserade": "färg-, lack-, limburkar vattenbaserade",
        "härdare metyl- etylketonperoxid": "härdare metyl-etylketonperoxid",
        "oljeavfall, fast osorterat emba": "oljeavfall, fast osorterat emballage",
    }

    def normalize(self, value: str) -> str:
        text = (value or "").replace("\xa0", " ")
        text = text.replace("–", "-").replace("×", "x")
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"\s*/\s*", "/", text)
        text = re.sub(r"\s*-\s*", "-", text)
        text = text.replace("m3", "m³")
        text = text.replace(" inkl ", " inkl. ")
        text = re.sub(r"\binkl\.\.", "inkl.", text)
        text = text.strip(" .;:")
        text = self.ALIASES.get(text, text)
        return text
