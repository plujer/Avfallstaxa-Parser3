"""Write detailed acceptance debug report."""

from __future__ import annotations

from pathlib import Path

from parser3.acceptance.acceptance_debugger import AcceptanceDebugResult


class AcceptanceDebugReporter:
    def write(self, result: AcceptanceDebugResult, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Parser Acceptance Debug Report",
            "",
            "Purpose: identify exactly which manually verified facit rows are missing.",
            "",
        ]

        for section in result.sections:
            lines.append(f"SECTION {section.section}")
            lines.append(f"Expected names: {len(section.expected_names)}")
            lines.append(f"Exported names: {len(section.exported_names)}")
            lines.append(f"Missing names: {len(section.missing_names)}")
            lines.append(f"Extra names: {len(section.extra_names)}")
            lines.append("")

            if section.missing_names:
                lines.append("MISSING")
                for name in section.missing_names:
                    lines.append(f"- {name}")
                    matches = section.possible_matches.get(name, [])
                    if matches:
                        lines.append("  possible parser names:")
                        for match in matches:
                            lines.append(f"    - {match}")
                lines.append("")

            if section.extra_names:
                lines.append("EXTRA EXPORTED")
                for name in section.extra_names:
                    lines.append(f"- {name}")
                lines.append("")

            if section.non_tax_candidates:
                lines.append("FOUND IN SEMANTIC ROWS BUT NOT EXPORTED")
                for candidate in section.non_tax_candidates:
                    lines.append(f"- {candidate}")
                lines.append("")

            lines.append("-" * 80)
            lines.append("")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
