"""Main parser entrypoint for Parser 3.0."""

from __future__ import annotations

import argparse
from pathlib import Path

from parser3.config_loader import load_config
from parser3.document import DocumentReader
from parser3.export import JsonExporter, TextReporter
from parser3.extractors import TaxRowExtractor
from parser3.headings import HeadingTreeBuilder
from parser3.rows import RowClassifier
from parser3.tables import SmartTableDetector
from parser3.utils.constants import APP_NAME, APP_VERSION
from parser3.utils.logger import get_logger


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Avfallstaxa Parser 3.0")
    arg_parser.add_argument("--word", help="Path to Word document (.docx)", default="")
    arg_parser.add_argument("--headings", action="store_true", help="Print detected heading tree")
    arg_parser.add_argument("--tables", action="store_true", help="Print detected tables and row classes")
    arg_parser.add_argument("--extract", action="store_true", help="Extract preliminary tax rows")
    args = arg_parser.parse_args()

    logger = get_logger("parser3")
    config = load_config()
    app = config.get("app", {})
    name = app.get("name", APP_NAME)
    version = app.get("version", APP_VERSION)

    logger.info("%s version %s", name, version)
    print("Avfallstaxa Parser 3.0 bootstrap OK")
    print(f"Config loaded: {name} {version}")

    if not args.word:
        return

    blocks = DocumentReader().read(Path(args.word))
    print(f"Document blocks read: {len(blocks)}")

    if args.headings:
        builder = HeadingTreeBuilder()
        roots = builder.build(blocks)
        flat = builder.flatten(roots)
        print(f"Headings detected: {len(flat)}")
        for node in flat:
            indent = "  " * (node.level - 1)
            print(f"{indent}{node.number} {node.title}")
        return

    if args.tables:
        tables = SmartTableDetector().detect(blocks)
        classifier = RowClassifier()
        print(f"Tables detected: {len(tables)}")
        for table in tables[:10]:
            print(f"TABLE {table.source} order={table.start_order} rows={len(table.rows)}")
            for row in table.rows[:8]:
                classified = classifier.classify(row)
                print(f"  {classified.row_type:10s} | {' | '.join(row)}")
        return

    if args.extract:
        tables = SmartTableDetector().detect(blocks)
        extractor = TaxRowExtractor()
        rows = []
        for table in tables:
            rows.extend(extractor.extract_from_rows(table.rows))
        JsonExporter().export(rows, "output/parser3_result.json")
        TextReporter().write(rows, "output/parser3_report.txt")
        print(f"Extracted preliminary tax rows: {len(rows)}")
        print("Output: output/parser3_result.json")
        print("Report: output/parser3_report.txt")
        return

    for block in blocks[:10]:
        print(f"{block.order:04d} | {block.kind} | {block.style} | {block.text[:100]}")
