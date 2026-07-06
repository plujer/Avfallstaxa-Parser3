from excel_builder.models import EdpExport, EdpExportRow, StandardTaxCatalog, StandardTaxRow
from excel_builder.standard import EdpStandardDeviationEngine


def test_edp_standard_deviation_engine_marks_same_code_ok():
    edp = EdpExport(municipality="Sorsele", source_path="edp.xlsx", rows=[
        EdpExportRow(strTaxekod="KOD1", strTaxebenamning="Test", strFaktor="ÅRPR", strTaxedelAvser="Taxedel")
    ])
    catalog = StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(source_sheet="Standard", row_number=2, strTaxekod="KOD1", strTaxebenamning="Test", strFaktor="ÅRPR", strTaxedelAvser="Taxedel")
    ])

    report = EdpStandardDeviationEngine().compare(edp, catalog)

    assert report.ok_count == 1
    assert report.review_count == 0


def test_edp_standard_deviation_engine_marks_factor_deviation_review():
    edp = EdpExport(municipality="Sorsele", source_path="edp.xlsx", rows=[
        EdpExportRow(strTaxekod="KOD1", strTaxebenamning="Test", strFaktor="ANNAN", strTaxedelAvser="Taxedel")
    ])
    catalog = StandardTaxCatalog(source_path="standard.xlsx", rows=[
        StandardTaxRow(source_sheet="Standard", row_number=2, strTaxekod="KOD1", strTaxebenamning="Test", strFaktor="ÅRPR", strTaxedelAvser="Taxedel")
    ])

    report = EdpStandardDeviationEngine().compare(edp, catalog)

    assert report.review_count == 1
    assert "Faktor avviker" in report.deviations[0].deviation_type
