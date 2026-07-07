from pathlib import Path

import pytest

from excel_builder.guards import (
    ImmutableMasterViolation,
    MasterGuard,
    MasterCopyManager,
    ProtectedRangeGuard,
    ProtectedRangeRule,
    column_in_rule,
    column_letter_to_index,
)


def test_column_range_helpers_support_excel_columns():
    assert column_letter_to_index("A") == 1
    assert column_letter_to_index("E") == 5
    assert column_letter_to_index("AA") == 27
    assert column_in_rule(1, "A:E") is True
    assert column_in_rule(5, "A:E") is True
    assert column_in_rule(6, "A:E") is False
    assert column_in_rule(20, "ALL") is True


def test_protected_range_guard_blocks_taxepunkter_a_to_e():
    guard = ProtectedRangeGuard([
        ProtectedRangeRule("Taxepunkter", "A:E", "Taxepunkter A:E är immutable."),
    ])

    with pytest.raises(ImmutableMasterViolation):
        guard.assert_write_allowed("Taxepunkter", 5)

    guard.assert_write_allowed("Taxepunkter", 6)


def test_master_guard_blocks_taxa_fran_edp_and_taxepunkter_template_columns():
    guard = MasterGuard()

    with pytest.raises(ImmutableMasterViolation):
        guard.assert_workbook_write_allowed("Taxa_från_edp", 1)

    with pytest.raises(ImmutableMasterViolation):
        guard.assert_workbook_write_allowed("Taxepunkter", 1)

    guard.assert_workbook_write_allowed("Taxepunkter", 6)


def test_master_guard_blocks_output_over_master_paths():
    guard = MasterGuard()

    with pytest.raises(ImmutableMasterViolation):
        guard.assert_output_path_allowed(guard.sources.excel_master)

    with pytest.raises(ImmutableMasterViolation):
        guard.assert_output_path_allowed(guard.sources.word_master)


def test_master_copy_manager_copies_without_changing_source(tmp_path):
    guard = MasterGuard()
    before = guard.fingerprint_masters()

    output = tmp_path / "ArbetsExcel_working_copy.xlsx"
    copied = guard.create_excel_working_copy(output)

    assert copied == output
    assert output.exists()
    guard.verify_masters_unchanged(before)


def test_master_copy_manager_refuses_to_overwrite_source(tmp_path):
    source = tmp_path / "master.xlsx"
    source.write_text("immutable", encoding="utf-8")
    manager = MasterCopyManager([source])

    with pytest.raises(ImmutableMasterViolation):
        manager.create_copy(source, source)
