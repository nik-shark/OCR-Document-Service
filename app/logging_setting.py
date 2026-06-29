import logging
import logging.config
import os
from pathlib import Path

import yaml

APP_DIR = Path(__file__).resolve().parent

DEFAULT_CONFIG = APP_DIR / "logging_config.yaml"
DEFAULT_LOG_DIR = APP_DIR.parent / "logs"


def setup_logging(service_name: str = "app") -> None:
    config_path = Path(os.getenv("LOG_CFG", DEFAULT_CONFIG))
    log_dir = Path(os.getenv("LOG_DIR", DEFAULT_LOG_DIR))
    log_dir.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format=(
                "%(asctime)s | %(levelname)-8s | "
                "%(name)s | %(message)s"
            ),
        )
        logging.getLogger(__name__).warning(
            "Logging config not found: %s", config_path
        )
        return

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    config["handlers"]["console"]["level"] = os.getenv(
        "CONSOLE_LEVEL", "DEBUG"
    )
    config["handlers"]["file"]["level"] = os.getenv(
        "LOG_LEVEL", "INFO"
    )
    config["handlers"]["file"]["filename"] = str(
        log_dir / f"{service_name}.log"
    )
    config["handlers"]["errors"]["filename"] = str(
        log_dir / f"{service_name}-errors.log"
    )

    logging.config.dictConfig(config)
