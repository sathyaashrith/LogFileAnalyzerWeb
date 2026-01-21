import logging
import os


def setup_logger(log_file_path: str = "logs/app.log") -> logging.Logger:
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    logger = logging.getLogger("LogAnalyzer")
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate logs if rerun in VS Code
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
