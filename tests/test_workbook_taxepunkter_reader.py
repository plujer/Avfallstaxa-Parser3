from openpyxl import Workbook
from excel_builder.io import WorkbookTaxepunkterReader


def test_workbook_taxepunkter_reader_reads_rows(tmp_path):
    path = tmp_path / "arbets.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Taxepunkter"
    ws.append([""])
    ws.append([""])
    ws.append([""])
    ws.append([""])
    ws.append(["Paragraf", "Paragrafnamn", "Taxapunkt", "Variant", "Enhet", "Taxakod", "Föreslagen Taxa"])
    ws.append(["6.1.2", "", "Asbest, emballerat", "", "kilogram", "KOD1", ""])
    wb.save(path)

    rows = WorkbookTaxepunkterReader().read(path)

    assert len(rows) == 1
    assert rows[0].tax_point == "Asbest, emballerat"
    assert rows[0].tax_code == "KOD1"
