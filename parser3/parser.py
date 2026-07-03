"""Main parser entrypoint for Parser 3.0 bootstrap."""

from __future__ import annotations

import argparse
from pathlib import Path

from parser3.config_loader import load_config
from parser3.document import DocumentReader
from parser3.utils.constants import APP_NAME, APP_VERSION
from parser3.utils.logger import get_logger


def main() -> None:
    arg_parser = argparse.ArgumentParser(description="Avfallstaxa Parser 3.0")
    arg_parser.add_argument("--word", help="Path to Word document (.docx)", default="")
    args = arg_parser.parse_args()

    logger = get_logger("parser3")
    config = load_config()
    app = config.get("app", {})
    name = app.get("name", APP_NAME)
    version = app.get("version", APP_VERSION)

    logger.info("%s version %s", name, version)
    print("Avfallstaxa Parser 3.0 bootstrap OK")
    print(f"Config loaded: {name} {version}")

    if args.word:
        blocks = DocumentReader().read(Path(args.word))
        print(f"Document blocks read: {len(blocks)}")
        for block in blocks[:10]:
            print(f"{block.order:04d} | {block.kind} | {block.style} | {block.text[:100]}")
