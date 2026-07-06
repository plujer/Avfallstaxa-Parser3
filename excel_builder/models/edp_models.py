"""Models for isolated EDP export runs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EdpExportRow:
    intRecnum: str = ""
    strTaxekod: str = ""
    strTaxebenamning: str = ""
    strProdukt: str = ""
    strDelProdukt: str = ""
    bytDelradnr: str = ""
    strFaktor: str = ""
    strTaxedelAvser: str = ""
    strEntreprenorkod: str = ""
    strRenhDistrKod: str = ""
    curNuvarandePris: str = ""
    datNuvarandePrisDatum: str = ""
    bolPrisPerTomning: str = ""
    strAvvikandeFormel: str = ""
    bolPriserInklMoms: str = ""
    bytMomskod: str = ""
    strFormel: str = ""


@dataclass
class EdpExport:
    municipality: str
    source_path: str
    rows: list[EdpExportRow] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        return len(self.rows)


@dataclass
class MunicipalityRunConfig:
    municipality: str
    edp_export_path: str
    parser_result_path: str = "output/reports/parser3_result.json"
    output_dir: str = ""
