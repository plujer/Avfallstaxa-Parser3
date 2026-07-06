from __future__ import annotations
import argparse
from pathlib import Path
from parser3.acceptance import AcceptanceReporter, AcceptanceRunner, FacitLoader
from parser3.config_loader import load_config
from parser3.context import ContextEngine
from parser3.diff import DiffEngine, ExplainReporter, PrecisionReporter
from parser3.document import DocumentReader
from parser3.excel import MasterExcelReader, ProfileReporter, WorkbookProfiler
from parser3.export import JsonExporter, TextReporter
from parser3.golden import GoldenMasterBuilder, GoldenMasterWriter
from parser3.headings import HeadingTreeBuilder
from parser3.pipeline import PipelineReporter, TaxPipeline
from parser3.rows import RowClassifier
from parser3.sections import SectionSummaryBuilder
from parser3.tables import SmartTableDetector
from parser3.utils.constants import APP_NAME, APP_VERSION
from parser3.utils.logger import get_logger
from parser3.validation import ValidationEngine

def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Avfallstaxa Parser 3.1")
    arg_parser.add_argument("--word", default="")
    arg_parser.add_argument("--master", default="")
    arg_parser.add_argument("--profile-master", action="store_true")
    arg_parser.add_argument("--headings", action="store_true")
    arg_parser.add_argument("--tables", action="store_true")
    arg_parser.add_argument("--context", action="store_true")
    arg_parser.add_argument("--semantic", action="store_true")
    arg_parser.add_argument("--acceptance", action="store_true")
    arg_parser.add_argument("--validate", action="store_true")
    arg_parser.add_argument("--build-golden", action="store_true")
    arg_parser.add_argument("--diff", action="store_true")
    arg_parser.add_argument("--explain", action="store_true")
    arg_parser.add_argument("--architecture", action="store_true")
    arg_parser.add_argument("--golden", default="golden_master/parser_facit.yaml")
    args = arg_parser.parse_args()

    logger = get_logger("parser3")
    config = load_config()
    app = config.get("app", {})
    name = app.get("name", APP_NAME)
    version = app.get("version", APP_VERSION)
    logger.info("%s version %s", name, version)
    print("Avfallstaxa Parser 3.1 bootstrap OK")
    print(f"Config loaded: {name} {version}")

    if args.profile_master:
        if not args.master:
            print("ERROR: --profile-master requires --master <xlsx path>")
            return
        profile = WorkbookProfiler().profile(args.master)
        ProfileReporter().write(profile, "output/master_profile_report.txt")
        best = profile.best_sheet
        print("Master profile report: output/master_profile_report.txt")
        if best:
            print(f"Best sheet: {best.sheet_name}")
            print(f"Detected columns: {best.detected_columns}")
        rows = MasterExcelReader().read(args.master)
        print(f"Master rows read: {len(rows)}")
        return

    if not args.word:
        return

    if args.semantic or args.acceptance or args.validate or args.build_golden or args.diff or args.explain or args.architecture:
        pipeline_result = TaxPipeline().run(args.word)
        blocks = pipeline_result.blocks
        rows = pipeline_result.tax_rows
        print(f"Document blocks read: {len(blocks)}")
        JsonExporter().export(rows, "output/parser3_result.json")
        TextReporter().write(rows, "output/parser3_report.txt")
        print(f"Semantic rows: {len(pipeline_result.semantic_rows)}")
        print(f"Semantic tax rows: {len(rows)}")
        print("Section summary:")
        for summary in SectionSummaryBuilder().build(rows):
            print(f"  {summary.section}: {summary.tax_count}")

        if args.architecture:
            PipelineReporter().write(pipeline_result, "output/parser3_architecture_report.txt")
            print("Architecture report: output/parser3_architecture_report.txt")

        if args.explain:
            ExplainReporter().write(pipeline_result.semantic_rows, "output/parser3_explain_report.txt")
            print("Explain report: output/parser3_explain_report.txt")

        if args.acceptance:
            expectations = FacitLoader().load_builtin()
            acceptance = AcceptanceRunner().run(rows, expectations)
            AcceptanceReporter().write(acceptance, "output/parser3_acceptance_report.txt")
            print(f"Acceptance passed: {acceptance.passed}")
            print(f"Acceptance expected total: {acceptance.expected_total}")
            print(f"Acceptance actual total: {acceptance.actual_total}")
            print("Acceptance report: output/parser3_acceptance_report.txt")

        if args.build_golden:
            data = GoldenMasterBuilder().from_tax_rows(rows)
            GoldenMasterWriter().write(data, "output/parser_facit_generated.yaml")
            print("Golden master draft: output/parser_facit_generated.yaml")

        if args.diff:
            if not args.master:
                print("ERROR: --diff requires --master <xlsx path>")
            else:
                profile = WorkbookProfiler().profile(args.master)
                ProfileReporter().write(profile, "output/master_profile_report.txt")
                expected = MasterExcelReader().read(args.master)
                print(f"Arbeets-Excel rows read: {len(expected)}")
                best = profile.best_sheet
                if best:
                    print(f"Arbets-Excel best sheet: {best.sheet_name}")
                    print(f"Arbets-Excel detected columns: {best.detected_columns}")
                diff = DiffEngine().compare(rows, expected)
                PrecisionReporter().write(diff, "output/parser3_precision_report.txt")
                print(f"Diff matched: {len(diff.matched)}")
                print(f"Diff missing: {len(diff.missing)}")
                print(f"Diff extra: {len(diff.extra)}")
                print(f"Diff passed: {diff.passed}")
                print("Precision report: output/parser3_precision_report.txt")

        if args.validate:
            validation = ValidationEngine().validate(rows, args.golden)
            print(f"Validation passed: {validation.passed}")
            for warning in validation.warnings:
                print(f"WARNING: {warning}")
            for error in validation.errors:
                print(f"ERROR: {error}")
        return

    blocks = DocumentReader().read(Path(args.word))
    print(f"Document blocks read: {len(blocks)}")

    if args.context:
        summary = ContextEngine().summary(blocks)
        print("Context section summary:")
        for section, count in summary.section_counts.items():
            print(f"  {section}: {count}")
        return

    if args.headings:
        builder = HeadingTreeBuilder()
        flat = builder.flatten(builder.build(blocks))
        print(f"Headings detected: {len(flat)}")
        for node in flat:
            print(f"{'  ' * (node.level - 1)}{node.number} {node.title}")
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

    for block in blocks[:10]:
        print(f"{block.order:04d} | {block.kind} | {block.style} | {block.text[:100]}")
