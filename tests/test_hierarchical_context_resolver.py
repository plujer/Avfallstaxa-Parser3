from excel_builder.context import ParserContextResolver
from excel_builder.models import ParserTaxRow


def test_hierarchical_context_resolver_resets_property_between_subsections():
    rows = [
        ParserTaxRow(section="2.1", tax_point="En- och tvåbostadshus"),
        ParserTaxRow(section="2.1", tax_point="Kärl 240 l", unit="kr/år"),
        ParserTaxRow(section="2.1", tax_point="Fritidshus"),
        ParserTaxRow(section="2.1", tax_point="Kärl 240 l", unit="kr/år"),
    ]

    report = ParserContextResolver().resolve(rows)

    assert report.total == 2
    assert report.rows[0].context.property_type_context == "En- och tvåbostadshus"
    assert report.rows[1].context.property_type_context == "Fritidshus"
    assert "En-" not in report.rows[1].enriched_row.tax_point


def test_hierarchical_context_resolver_does_not_emit_structure_rows_as_tax_rows():
    rows = [
        ParserTaxRow(section="2.1", tax_point="En- och tvåbostadshus"),
        ParserTaxRow(section="2.1", tax_point="Fritidshus"),
        ParserTaxRow(section="2.1", tax_point="Kärl 190 l restavfall", unit="kr/år"),
    ]

    report = ParserContextResolver().resolve(rows)

    assert report.total == 1
    assert report.rows[0].original_row.tax_point == "Kärl 190 l restavfall"
    assert report.rows[0].context.hierarchy_path == "Fritidshus"


def test_hierarchical_context_resolver_uses_current_section_after_section_change():
    rows = [
        ParserTaxRow(section="5.1", tax_point="Extra tömning", unit="tillfälle"),
        ParserTaxRow(section="6.1.2", tax_point="Fönster med karm"),
        ParserTaxRow(section="6.1.2", tax_point="Per styck", unit="kr/st"),
    ]

    report = ParserContextResolver().resolve(rows)

    assert report.total == 2
    assert report.rows[0].context.section_context == "Slam"
    assert report.rows[1].context.section_context == "Verksamhetsavfall"
    assert "Slam" not in report.rows[1].enriched_row.tax_point
    assert report.rows[1].context.hierarchy_path == "Fönster med karm"
