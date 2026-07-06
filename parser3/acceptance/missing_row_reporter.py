"""Write missing row diagnostics report."""

from __future__ import annotations

from pathlib import Path

from parser3.acceptance.missing_row_diagnostics import MissingDiagnosticsResult


class MissingRowReporter:
    def write(self, result: MissingDiagnosticsResult, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "Parser Missing Row Diagnostics",
            "",
            f"Missing diagnostics: {len(result.diagnostics)}",
            "",
        ]

        for item in result.diagnostics:
            lines.append("=" * 100)
            lines.append(f"SECTION: {item.section}")
            lines.append(f"EXPECTED: {item.expected_name}")
            lines.append(f"NORMALIZED EXPECTED: {item.normalized_expected}")
            lines.append("")

            lines.append("EXACT SEMANTIC HITS")
            if item.exact_semantic_hits:
                for line in item.exact_semantic_hits:
                    lines.append(f"- {line}")
            else:
                lines.append("- none")
            lines.append("")

            lines.append("FUZZY SEMANTIC HITS")
            if item.fuzzy_semantic_hits:
                for line in item.fuzzy_semantic_hits:
                    lines.append(f"- {line}")
            else:
                lines.append("- none")
            lines.append("")

            lines.append("NEARBY / SHARED-WORD SEMANTIC ROWS")
            if item.nearby_semantic_rows:
                for line in item.nearby_semantic_rows:
                    lines.append(f"- {line}")
            else:
                lines.append("- none")
            lines.append("")

            lines.append("SIMILAR EXPORTED ROWS")
            if item.exported_similar_rows:
                for line in item.exported_similar_rows:
                    lines.append(f"- {line}")
            else:
                lines.append("- none")
            lines.append("")

        out.write_text("\n".join(lines), encoding="utf-8")
        return out
