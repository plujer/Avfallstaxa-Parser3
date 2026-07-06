"""Write parser acceptance report."""

from __future__ import annotations

from pathlib import Path

from parser3.acceptance.acceptance_models import AcceptanceResult


class AcceptanceReporter:
    def write(self, result: AcceptanceResult, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Parser Acceptance Report",
            "",
            f"Expected total in verified sections: {result.expected_total}",
            f"Actual total in verified sections: {result.actual_total}",
            f"Passed: {result.passed}",
            "",
            "Sections:",
        ]

        for section in result.sections:
            status = "OK" if section.passed else "FAIL"
            lines.append(
                f"- {section.section}: {status} "
                f"(expected {section.expected_count}, actual {section.actual_count})"
            )

            if section.missing_required:
                lines.append("  Missing required:")
                for name in section.missing_required:
                    lines.append(f"    - {name}")

            if section.wrongly_exported_ignored:
                lines.append("  Wrongly exported ignored rows:")
                for name in section.wrongly_exported_ignored:
                    lines.append(f"    - {name}")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
