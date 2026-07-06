"""Detailed manually verified facit catalog.

Important:
Only add rows that have been manually verified and approved.
This catalog is used to identify exactly which expected tax rows are missing.
"""

from __future__ import annotations


class FacitCatalog:
    def rows_by_section(self) -> dict[str, list[str]]:
        return {
            "6.1.2": [
                "Tonerkassetter, utan elektronik/chip",
                "Oljeemulsion, emballerat",
                "Förorenad olja innehållande PCB",
                "Oljeavskiljarslam",
                "Diesel",
                "Bensinrester",
                "Hydralslang, med/utan koppling",
                "Förpackningar, tömde ej rengjorda",
                "Oljeavfall, fast osorterat emba",
                "Absorbermedel, filtermaterial",
                "Oljefilter",
                "Bromsvätska",
                "Transformator, kondensator med PCB",
                "Fogskum",
                "Halon",
                "Koldioxid",
                "Brandsläckare",
                "Helium",
                "Tändare",
                "Syrgas",
                "Oxiderande fast ämne/vätska",
                "Klorex",
                "Aerosoler isocyanat, bekämpning",
                "Gasol inkl tub",
                "Gasol, blå programmet",
                "Giftig organisk vätska",
                "Småkemikalier, ej Hg-haltiga",
                "Giftig oorganisk vätska",
                "Oxidationsmedel, flytande",
                "Asbest, emballerat",
                "Smittförande avfall",
                "Lösningsmedel",
                "Väteperoxid",
                "Flourvätesyra",
                "Svavelsyra",
                "Salpetersyra",
                "Surt oorganisk fast ämne",
                "Surt organisk fast ämne",
                "Surt oorganisk vätska",
                "Surt organisk vätska",
                "Ammoniaklösning",
                "Alkaliskt avfall fast",
                "Basiskt organiskt fast/flytande",
                "Fotokemikalier",
                "Bekämpningsmedel aerosoler",
                "Bekämpningsmedel fast",
                "Bekämpningsmedel flytande",
                "Kvicksilverhaltigt avfall",
                "Kvicksilver i föremål",
                "Oljehaltigt avfall (ej PCB)",
                "Olja förorenad (ej PCB)",
                "Färg-, lack-, limburkar lösning",
                "Färg-, lack-, limburkar lösning aerosoler",
                "Isocyanater",
                "Härdare metyl- etylketonperoxid",
                "Härdare dibenzoylperoxid",
                "Färg-,lack-, limburkar vattenbaserade",
                "Tensida alkaliska flytande avfall",
                "Rengöring/vaskmedel fast",
                "Alkaliska flytande avfall",
                "Cytotoxiska läkemedel, cytostat",
                "Rökdetektor med andra isotoper",
                "Rökdetektor med Am 241",
            ],
            # 6.1.1, 6.1.3 and 6.1.4 are count-verified in this block.
            # Full name catalogs should be added only after manual verification.
        }
