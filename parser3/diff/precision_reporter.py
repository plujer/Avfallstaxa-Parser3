from pathlib import Path
from parser3.diff.diff_engine import DiffResult

class PrecisionReporter:
    def write(self, result: DiffResult, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "Parser 3.0 precision report",
            "",
            f"Matched: {len(result.matched)}",
            f"Missing: {len(result.missing)}",
            f"Extra: {len(result.extra)}",
            f"Passed: {result.passed}",
            "",
        ]
        if result.missing:
            lines.append("MISSING")
            for item in result.missing:
                lines.append(f"- {item.section} | {item.name} | {item.variant} | {item.unit} | {item.reason}")
            lines.append("")
        if result.extra:
            lines.append("EXTRA")
            for item in result.extra:
                lines.append(f"- {item.section} | {item.name} | {item.variant} | {item.unit} | {item.reason}")
        out.write_text("\n".join(lines), encoding="utf-8")
        return out
