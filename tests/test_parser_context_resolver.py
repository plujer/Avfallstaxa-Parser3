from excel_builder.context import ParserContextResolver
from excel_builder.models import ParserTaxRow


def test_context_resolver_enriches_short_row_with_previous_context():
    rows = [
        ParserTaxRow(section="2.1", tax_point="En- och tvåbostadshus"),
        ParserTaxRow(section="2.1", tax_point="Kärl 240 l", unit=""),
    ]

    report = ParserContextResolver().resolve(rows)

    assert report.total == 1
    assert "En-" in report.rows[0].enriched_row.tax_point or "tvåbostadshus" in report.rows[0].enriched_row.tax_point
    assert report.rows[0].context.property_type_context == "En- och tvåbostadshus"


def test_context_resolver_keeps_section_context():
    rows = [ParserTaxRow(section="5.1", tax_point="Extra tömning", unit="tillfälle")]

    report = ParserContextResolver().resolve(rows)

    assert report.rows[0].context.section_context == "Slam"
    assert "Slam" in report.rows[0].enriched_row.tax_point


def test_context_resolver_counts_enriched_rows():
    rows = [ParserTaxRow(section="2.1", tax_point="Kärl 190 l restavfall")]
    report = ParserContextResolver().resolve(rows)

    assert report.enriched_count >= 1
