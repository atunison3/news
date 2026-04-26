import logging
from datetime import datetime
from pathlib import Path


def str_to_dt(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def dt_to_str(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


def setup_logger(name: str = 'news_app') -> logging.Logger:
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / 'app.log'

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # avoid duplicate handlers on reload

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger