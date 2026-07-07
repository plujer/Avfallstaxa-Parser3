from excel_builder.document import DocumentStructureEngine
from excel_builder.models import DocumentRowType, ParserTaxRow


def test_document_structure_engine_marks_property_headings_as_subsections():
    rows = [
        ParserTaxRow(section="2.1", tax_point="En- och tvåbostadshus", price="1 650,00 kr"),
        ParserTaxRow(section="2.1", tax_point="Fritidshus", price="XX kr"),
        ParserTaxRow(section="2.1", tax_point="Verksamhet", price="XX kr"),
        ParserTaxRow(section="2.1", tax_point="Lägenhet i flerbostadshus", unit="lägenhet", price="XX kr"),
    ]

    report = DocumentStructureEngine().classify(rows)

    assert report.total == 4
    assert report.count(DocumentRowType.SUBSECTION) == 4
    assert report.count(DocumentRowType.TAX_NODE) == 0


def test_document_structure_engine_keeps_real_tax_rows_as_tax_nodes():
    rows = [
        ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l (mat-/restavfall)", unit="kärl", price="XX kr"),
        ParserTaxRow(section="6.1.2", tax_point="Asbest, emballerat", unit="kilogram", price=""),
    ]

    report = DocumentStructureEngine().classify(rows)

    assert report.count(DocumentRowType.TAX_NODE) == 2
    assert [row.tax_point for row in report.tax_rows] == [row.tax_point for row in rows]


def test_document_structure_engine_filters_only_tax_nodes():
    rows = [
        ParserTaxRow(section="2.1", tax_point="En- och tvåbostadshus", price="1 650,00 kr"),
        ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l (mat-/restavfall)", unit="kärl", price="XX kr"),
    ]

    tax_rows = DocumentStructureEngine().filter_tax_nodes(rows)

    assert len(tax_rows) == 1
    assert tax_rows[0].tax_point == "Kärl 240 l (mat-/restavfall)"
