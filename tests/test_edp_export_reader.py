from openpyxl import Workbook

from excel_builder.edp import EdpExportReader


def test_edp_export_reader_reads_edp_export(tmp_path):
    path = tmp_path / "edp.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Blad1"
    ws.append(["Rapport"])
    ws.append([
        "intRecnum", "strTaxekod", "strTaxebenamning", "strProdukt", "strDelProdukt",
        "bytDelradnr", "strFaktor", "strTaxedelAvser", "strEntreprenorkod",
        "strRenhDistrKod", "curNuvarandePris", "datNuvarandePrisDatum",
        "bolPrisPerTomning", "strAvvikandeFormel", "bolPriserInklMoms",
        "bytMomskod", "strFormel",
    ])
    ws.append([1, "KOD1", "Testbenämning", "RENH", "HUSH", 1, "ÅRPR", "Taxedel", "", "", 100, 45658, 0, "", "-", 1, "FORMEL"])
    wb.save(path)

    export = EdpExportReader().read(path, "Testkommun")

    assert export.municipality == "Testkommun"
    assert export.row_count == 1
    assert export.rows[0].strTaxekod == "KOD1"
    assert export.rows[0].curNuvarandePris == "100"
