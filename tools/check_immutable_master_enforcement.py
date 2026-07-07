from __future__ import annotations

from pathlib import Path
import json

from excel_builder.guards import MasterGuard, ImmutableMasterViolation


def main() -> int:
    guard = MasterGuard()
    out_dir = Path("output/diagnostics")
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "immutable_master_enforcement_report.txt"
    json_path = out_dir / "immutable_master_enforcement.json"

    checks: list[tuple[str, bool, str]] = []

    for name, path in [("word_master", guard.sources.word_master), ("excel_master", guard.sources.excel_master)]:
        try:
            guard.assert_output_path_allowed(path)
        except ImmutableMasterViolation as exc:
            checks.append((f"block_output_to_{name}", True, str(exc)))
        else:
            checks.append((f"block_output_to_{name}", False, "Master output was not blocked."))

    try:
        guard.assert_workbook_write_allowed("Taxa_från_edp", 1)
    except ImmutableMasterViolation as exc:
        checks.append(("block_taxa_fran_edp", True, str(exc)))
    else:
        checks.append(("block_taxa_fran_edp", False, "Taxa_från_edp write was not blocked."))

    try:
        guard.assert_workbook_write_allowed("Taxepunkter", 5)
    except ImmutableMasterViolation as exc:
        checks.append(("block_taxepunkter_a_to_e", True, str(exc)))
    else:
        checks.append(("block_taxepunkter_a_to_e", False, "Taxepunkter A:E write was not blocked."))

    try:
        guard.assert_workbook_write_allowed("Taxepunkter", 6)
    except ImmutableMasterViolation as exc:
        checks.append(("allow_taxepunkter_from_f", False, str(exc)))
    else:
        checks.append(("allow_taxepunkter_from_f", True, "Taxepunkter column F+ allowed."))

    ok = all(item[1] for item in checks)
    lines = ["Immutable Master Enforcement Report", "", f"Status: {'OK' if ok else 'FAILED'}", ""]
    for check_name, passed, message in checks:
        lines.append(f"{'OK' if passed else 'FAIL'} | {check_name} | {message}")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "status": "OK" if ok else "FAILED",
                "master_version": guard.sources.master_version,
                "checks": [
                    {"name": name, "passed": passed, "message": message} for name, passed, message in checks
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
