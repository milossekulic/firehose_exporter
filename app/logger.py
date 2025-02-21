# app/logger.py
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    general_handler = RotatingFileHandler(
        "file_processor.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    general_handler.setFormatter(log_formatter)
    general_handler.setLevel(logging.INFO)

    error_handler = RotatingFileHandler(
        "file_processor_errors.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    error_handler.setFormatter(log_formatter)
    error_handler.setLevel(logging.ERROR)

    not_sent_records_handler = RotatingFileHandler(
        "file_processor_not_sent_records.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
    )
    not_sent_records_handler.setFormatter(log_formatter)
    not_sent_records_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[general_handler, error_handler, not_sent_records_handler],
    )


setup_logging()
