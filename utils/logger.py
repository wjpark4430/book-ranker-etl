import logging
import os
from datetime import datetime


def setup_logger(name: str, level=logging.INFO, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    log_filename = os.path.join(log_dir, f"{datetime.now():%Y-%m-%d}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # 콘솔용 핸들러: 모든 로그 출력
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 파일용 핸들러: WARNING 이상만 저장
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
