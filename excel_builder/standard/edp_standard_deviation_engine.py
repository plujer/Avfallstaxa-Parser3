"""Compare municipality EDP export with standard tax catalog.

Important:
This engine never changes Taxa_från_edp. It only writes review material to
EDP_Avviker_Standard.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from excel_builder.matching import MatchNormalizer
from excel_builder.models import EdpExport, EdpExportRow, StandardTaxCatalog, StandardTaxRow


@dataclass
class EdpStandardDeviation:
    municipality: str
    edp_row: EdpExportRow
    standard_row: StandardTaxRow | None
    status: str
    score: float
    deviation_type: str
    recommendation: str


@dataclass
class EdpStandardDeviationReport:
    municipality: str
    deviations: list[EdpStandardDeviation] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.deviations)

    @property
    def review_count(self) -> int:
        return sum(1 for item in self.deviations if item.status == "REVIEW")

    @property
    def ok_count(self) -> int:
        return sum(1 for item in self.deviations if item.status == "OK")


class EdpStandardDeviationEngine:
    OK_THRESHOLD = 0.92
    REVIEW_THRESHOLD = 0.75

    def __init__(self) -> None:
        self.normalizer = MatchNormalizer()

    def compare(self, edp_export: EdpExport, catalog: StandardTaxCatalog) -> EdpStandardDeviationReport:
        report = EdpStandardDeviationReport(municipality=edp_export.municipality)
        report.warnings.extend(catalog.warnings)
        report.warnings.extend(edp_export.warnings)

        standard_by_code = {
            self.normalizer.normalize(row.strTaxekod): row
            for row in catalog.rows
            if row.strTaxekod
        }

        for edp_row in edp_export.rows:
            code_key = self.normalizer.normalize(edp_row.strTaxekod)
            standard_row = standard_by_code.get(code_key)

            if standard_row:
                deviation_type = self._compare_same_code(edp_row, standard_row)
                status = "OK" if deviation_type == "" else "REVIEW"
                recommendation = (
                    "Ingen åtgärd. Befintlig kommun-EDP behålls."
                    if status == "OK"
                    else "Granska avvikelse. Ändra inte Taxa_från_edp automatiskt."
                )
                report.deviations.append(
                    EdpStandardDeviation(
                        municipality=edp_export.municipality,
                        edp_row=edp_row,
                        standard_row=standard_row,
                        status=status,
                        score=1.0,
                        deviation_type=deviation_type or "Ingen avvikelse",
                        recommendation=recommendation,
                    )
                )
                continue

            best = self._best_name_match(edp_row, catalog.rows)
            if best is None:
                report.deviations.append(
                    EdpStandardDeviation(
                        municipality=edp_export.municipality,
                        edp_row=edp_row,
                        standard_row=None,
                        status="REVIEW",
                        score=0.0,
                        deviation_type="EDP-taxekod saknas i standardtaxor",
                        recommendation="Behåll kommun-EDP. Granska om standardtaxa bör dokumenteras som referens.",
                    )
                )
                continue

            standard_row, score = best
            if score >= self.REVIEW_THRESHOLD:
                report.deviations.append(
                    EdpStandardDeviation(
                        municipality=edp_export.municipality,
                        edp_row=edp_row,
                        standard_row=standard_row,
                        status="REVIEW",
                        score=score,
                        deviation_type="Taxekod saknas i standard men benämning liknar standardtaxa",
                        recommendation="Granska manuell koppling. Ändra inte befintlig EDP automatiskt.",
                    )
                )
            else:
                report.deviations.append(
                    EdpStandardDeviation(
                        municipality=edp_export.municipality,
                        edp_row=edp_row,
                        standard_row=None,
                        status="REVIEW",
                        score=score,
                        deviation_type="Ingen tydlig standardtaxa hittad",
                        recommendation="Behåll kommun-EDP. Ingen standardrekommendation.",
                    )
                )

        return report

    def _compare_same_code(self, edp_row: EdpExportRow, standard_row: StandardTaxRow) -> str:
        deviations: list[str] = []

        if self._n(edp_row.strTaxebenamning) and self._n(standard_row.strTaxebenamning):
            score = SequenceMatcher(None, self._n(edp_row.strTaxebenamning), self._n(standard_row.strTaxebenamning)).ratio()
            if score < self.OK_THRESHOLD:
                deviations.append("Benämning avviker")

        if self._n(edp_row.strFaktor) != self._n(standard_row.strFaktor) and standard_row.strFaktor:
            deviations.append("Faktor avviker")

        if self._n(edp_row.strTaxedelAvser) != self._n(standard_row.strTaxedelAvser) and standard_row.strTaxedelAvser:
            deviations.append("Taxedel avviker")

        if self._n(edp_row.strFormel) != self._n(standard_row.strFormel) and standard_row.strFormel:
            deviations.append("Formel avviker")

        return ", ".join(deviations)

    def _best_name_match(self, edp_row: EdpExportRow, standard_rows: list[StandardTaxRow]) -> tuple[StandardTaxRow, float] | None:
        edp_name = self._n(edp_row.strTaxebenamning)
        if not edp_name:
            return None

        best_row: StandardTaxRow | None = None
        best_score = 0.0

        for standard_row in standard_rows:
            standard_name = self._n(standard_row.strTaxebenamning)
            if not standard_name:
                continue
            score = SequenceMatcher(None, edp_name, standard_name).ratio()
            if score > best_score:
                best_score = score
                best_row = standard_row

        if best_row is None:
            return None
        return best_row, best_score

    def _n(self, value: str) -> str:
        return self.normalizer.normalize(value)
