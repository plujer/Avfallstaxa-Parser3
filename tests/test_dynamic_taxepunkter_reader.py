from openpyxl import Workbook

from excel_builder.rules import DynamicTaxepunkterReader, MasterRuleRepositoryReader


def create_master(path):
    wb = Workbook()

    ws = wb.active
    ws.title = "Taxepunkter"
    ws.append(["Titel"])
    ws.append([""])
    ws.append([""])
    ws.append([""])
    ws.append(["Paragraf", "Paragrafnamn", "Taxapunkt", "Variant", "Enhet", "Taxakod", "Föreslagen Taxa", "Faktor", "Formel", "Taxedel"])
    ws.append(["6.1.2", "ÅVC", "Asbest, emballerat", "", "kilogram", "EDP1", "", "VIKG", "FORMEL1", "Taxedel"])
    ws.append(["6.1.3", "ÅVC", "Gips", "", "kilogram", "", "Föreslagen rad", "VIKG", "", ""])

    edp = wb.create_sheet("Taxa_från_edp")
    edp.append(["meta"])
    edp.append(["strTaxekod", "strTaxebenamning", "strFaktor", "strTaxedelAvser", "strFormel"])
    edp.append(["EDP2", "Gips", "VIKG", "Kilogram", "FORMEL2"])

    wb.save(path)


def test_dynamic_taxepunkter_reader_uses_detected_header_row(tmp_path):
    path = tmp_path / "master.xlsx"
    create_master(path)

    rules, warnings = DynamicTaxepunkterReader().read(path)

    assert not warnings
    assert len(rules) == 2
    assert rules[0].row_number == 6
    assert rules[0].tax_code == "EDP1"
    assert rules[0].rule_type == "TAXEPUNKT"


def test_master_rule_repository_uses_dynamic_taxepunkter_reader(tmp_path):
    path = tmp_path / "master.xlsx"
    create_master(path)

    repo = MasterRuleRepositoryReader().read(path)

    assert len(repo.taxepunkt_rules) == 2
    assert len(repo.edp_rules) == 1
    assert repo.taxepunkt_rules[0].tax_code == "EDP1"
