"""Extract tax rows while preserving table cells."""

from __future__ import annotations

from parser3.models import TaxRow
from parser3.extractors.metadata_extractor import MetadataExtractor
from parser3.tables2.price_cell_detector import PriceCellDetector
from parser3.tables2.table_row_builder import TableRowBuilder
from parser3.tables2.table_shape_detector import TableShapeDetector
from parser3.taxonomy.unit_detector import UnitDetector


class StructuredTaxExtractor:
    def __init__(self) -> None:
        self.builder = TableRowBuilder()
        self.price_detector = PriceCellDetector()
        self.shape = TableShapeDetector()
        self.unit_detector = UnitDetector()
        self.metadata = MetadataExtractor()

    def extract_table(
        self,
        rows: list[list[str]],
        chapter: str = "",
        section: str = "",
        group: str = "",
    ) -> list[TaxRow]:
        result: list[TaxRow] = []
        current_variants: dict[int, str] = {}
        current_unit = ""

        for raw_row in rows:
            table_row = self.builder.build(raw_row)
            cells = table_row.raw_cells
            if not any(cells):
                continue

            if self.shape.is_header(cells):
                current_variants.update(self.shape.variants_from_header(cells))
                unit = self.shape.unit_from_header(cells)
                if unit:
                    current_unit = unit
                continue

            price_cells = self.price_detector.price_cells(cells)
            if not price_cells:
                continue

            name = self._name_from_cells(cells)
            if not name:
                continue

            for idx, price in price_cells:
                variant = current_variants.get(idx, "")
                unit = current_unit or self.unit_detector.detect(cells, " ".join(cells))
                result.append(
                    TaxRow(
                        chapter=chapter,
                        section=section,
                        group=group,
                        name=name,
                        variant=variant,
                        unit=unit,
                        price=price,
                        ewc=self.metadata.extract_ewc(cells),
                        un_number=self.metadata.extract_un(cells),
                        export=True,
                    )
                )

        return result

    def _name_from_cells(self, cells: list[str]) -> str:
        # Prefer the first cell, but if it is empty use the first non-price metadata-free cell.
        first = (cells[0] if cells else "").strip()
        if first and not self.price_detector.is_price_cell(first):
            return first

        for cell in cells:
            clean = (cell or "").strip()
            if not clean:
                continue
            if self.price_detector.is_price_cell(clean):
                continue
            if clean.lower() in {"ewc kod", "un-nr", "enhet", "pris"}:
                continue
            return clean
        return ""
