import logging
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "etl", level=logging.INFO):
    log_dir = Path("logs") / name
    log_dir.mkdir(parents=True, exist_ok=True)

    log_filename = log_dir / f"{datetime.now():%Y-%m-%d}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 중복 핸들러 방지
    if not logger.handlers:
        # 콘솔 핸들러 (INFO 이상)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 파일 핸들러 (WARNING 이상)
        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setLevel(logging.WARNING)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
