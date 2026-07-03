"""Main parser entrypoint for Parser 3.0 bootstrap."""

from __future__ import annotations

from parser3.config_loader import load_config
from parser3.utils.constants import APP_NAME, APP_VERSION
from parser3.utils.logger import get_logger


def main() -> None:
    logger = get_logger("parser3")
    config = load_config()
    app = config.get("app", {})
    name = app.get("name", APP_NAME)
    version = app.get("version", APP_VERSION)

    logger.info("%s version %s", name, version)
    print("Avfallstaxa Parser 3.0 bootstrap OK")
    print(f"Config loaded: {name} {version}")
