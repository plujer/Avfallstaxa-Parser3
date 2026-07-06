from openpyxl import Workbook

from excel_builder.rules import RulebookReader, EdpRuleValidator


def test_rulebook_reader_reads_rule_sheets(tmp_path):
    path = tmp_path / "arbets.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "03_Arbetsflöde"
    ws.append(["7", "Matcha mot Taxa_från_edp", "Använd matchningsordningen strTaxekod → strTaxebenamning → strTaxedelAvser → strFaktor."])

    wb.create_sheet("Dokumentation_Taxepunkter")
    wb["Dokumentation_Taxepunkter"].append(["F", "Taxakod", "Taxa_från_edp[strTaxekod]", "Taxakod får bara vara bekräftad EDP-kod."])

    rulebook = RulebookReader().read(path)

    assert rulebook.count >= 2
    assert rulebook.contains_text("strTaxekod")
    assert rulebook.contains_text("Taxa_från_edp")


def test_edp_rule_validator_detects_missing_terms():
    path_rulebook = RulebookReader().read("does_not_exist.xlsx")
    warnings = EdpRuleValidator().validate(path_rulebook)

    assert warnings
