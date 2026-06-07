import logging
from pathlib import Path

# Ensure data directory exists
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DATA_DIR / "jarvis.log"

logger = logging.getLogger("jarvis")
logger.setLevel(logging.DEBUG)

# Create file handler which logs debug messages
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Create console handler with a higher log level for print statements
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("JARVIS: %(message)s")
console_handler.setFormatter(console_formatter)

# Avoid duplicate handlers if imported multiple times
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def log(message: str) -> None:
    """Print message to console and write to log file for backward compatibility."""
    logger.info(message)


def debug(message: str) -> None:
    logger.debug(message)


def info(message: str) -> None:
    logger.info(message)


def warning(message: str) -> None:
    logger.warning(message)


def error(message: str, exc_info: bool = False) -> None:
    logger.error(message, exc_info=exc_info)
