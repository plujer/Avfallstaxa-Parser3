from excel_builder.models import ParserTaxRow
from excel_builder.persistent_identity import PersistentTaxIdentityEngine


def test_persistent_tax_identity_survives_section_move():
    original = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")
    moved = ParserTaxRow(section="2.2.9", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")

    report = PersistentTaxIdentityEngine().build([original, moved])

    assert report.total == 2
    assert report.identities[0].content_fingerprint == report.identities[1].content_fingerprint
    assert report.identities[0].section_bound_word_tax_id != report.identities[1].section_bound_word_tax_id
    assert report.identities[0].persistent_tax_id.endswith("-01")
    assert report.identities[1].persistent_tax_id.endswith("-02")
    assert "inte automatiskt fel" in report.identities[0].comment


def test_persistent_tax_identity_changes_when_business_meaning_changes():
    first = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")
    second = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="månadsvis", unit="kr")

    report = PersistentTaxIdentityEngine().build([first, second])

    assert report.identities[0].content_fingerprint != report.identities[1].content_fingerprint
    assert report.identities[0].persistent_tax_id != report.identities[1].persistent_tax_id


def test_persistent_tax_identity_not_edp_tax_code():
    row = ParserTaxRow(section="2.2.1", tax_point="Kärl 240 l", variant="14 dagar", unit="kr")

    report = PersistentTaxIdentityEngine().build([row])

    assert report.identities[0].persistent_tax_id.startswith("PTX-")
    assert not report.identities[0].persistent_tax_id.startswith("KÄ")
