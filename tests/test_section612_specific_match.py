from parser3.extractors import Section612Extractor
from parser3.trace import TraceStore


def test_section612_prefers_longest_specific_match():
    store = TraceStore()
    text = (
        "Skrymmande avfall till energiåtervinning större än 20*20*80 "
        "Skrymmande avfall till energiåtervinning större än 20*20*80 "
        "200307 200307 kilogram kilogram"
    )

    rows = Section612Extractor(trace_store=store).extract_line(text, chapter="6", section="6.1.2")

    assert len(rows) == 1
    assert rows[0].name == "Skrymmande avfall till energiåtervinning större än 20×20×80"
    assert store.events[-1].best_match == "Skrymmande avfall till energiåtervinning större än 20×20×80"
    assert "longest substring match" in store.events[-1].reason or "exact match" in store.events[-1].reason


def test_section612_does_not_let_short_substring_win():
    rows = Section612Extractor().extract_line(
        "Skrymmande avfall till energiåtervinning större än 20*20*80",
        chapter="6",
        section="6.1.2",
    )
    assert rows[0].name != "Avfall till energiåtervinning"
