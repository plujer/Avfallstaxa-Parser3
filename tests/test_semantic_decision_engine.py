from excel_builder.decision import SemanticDecisionEngine
from excel_builder.models import (
    ParserTaxRow,
    SemanticCandidate,
    TaxSemanticProfile,
    TaxSemanticProfileKey,
)


def profile(source, source_id, tax_code="", standard_tax_code="", **key):
    return TaxSemanticProfile(
        source=source,
        source_id=source_id,
        key=TaxSemanticProfileKey(**key),
        tax_code=tax_code,
        standard_tax_code=standard_tax_code,
    )


def candidate(word, cand, score):
    return SemanticCandidate(word_profile=word, candidate_profile=cand, score=score, status="REVIEW_REQUIRED")


def test_semantic_decision_engine_prefers_edp_with_source_bonus():
    parser_rows = [ParserTaxRow(section="2.1", tax_point="Kärl 190 L restavfall")]
    word = profile("WORD", "WORD:1", waste_type="Restavfall")

    standard = profile("STANDARD", "STD:1", standard_tax_code="STD1", waste_type="Restavfall")
    edp = profile("RULE:EDP", "EDP:1", tax_code="EDP1", waste_type="Restavfall")

    decisions = SemanticDecisionEngine().decide(
        parser_rows,
        [candidate(word, standard, 0.90), candidate(word, edp, 0.89)],
    )

    assert decisions.decisions[0].source == "Kommunens EDP"


def test_semantic_decision_engine_standard_proposal_when_standard_best():
    parser_rows = [ParserTaxRow(section="2.1", tax_point="Kärl 190 L restavfall")]
    word = profile("WORD", "WORD:1", waste_type="Restavfall")
    standard = profile("STANDARD", "STD:1", standard_tax_code="STD1", waste_type="Restavfall")

    decisions = SemanticDecisionEngine().decide(parser_rows, [candidate(word, standard, 0.90)])

    assert decisions.standard_proposal == 1
    assert decisions.decisions[0].status == "STANDARD_PROPOSAL"


def test_semantic_decision_engine_marks_ambiguous_top_candidates_review():
    parser_rows = [ParserTaxRow(section="2.1", tax_point="Kärl 190 L restavfall")]
    word = profile("WORD", "WORD:1", waste_type="Restavfall")
    standard1 = profile("STANDARD", "STD:1", standard_tax_code="STD1", waste_type="Restavfall")
    standard2 = profile("STANDARD", "STD:2", standard_tax_code="STD2", waste_type="Restavfall")

    decisions = SemanticDecisionEngine().decide(
        parser_rows,
        [candidate(word, standard1, 0.90), candidate(word, standard2, 0.89)],
    )

    assert decisions.review_required == 1
    assert "för nära" in decisions.decisions[0].rule
