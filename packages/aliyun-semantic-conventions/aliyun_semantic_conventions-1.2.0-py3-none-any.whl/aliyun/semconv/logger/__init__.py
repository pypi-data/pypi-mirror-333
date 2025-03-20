import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/aliyun-python-agent.log"

LOG_MAX_BYTES = "LOG_MAX_BYTES"
LOG_BACKUP_COUNT = "LOG_BACKUP_COUNT"


def getLogger(logger_name: str, level=logging.INFO):
    """Function to setup a logger; can be called from any module in the code."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False
    flag = check_log_file()
    if not flag:
        return logger
    handler = RotatingFileHandler(LOG_FILE, maxBytes=get_max_bytes(), backupCount=get_backup_count())
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_max_bytes() -> int:
    max_m_bytes = 300
    size_str = os.getenv(LOG_MAX_BYTES, "300")
    if size_str is not None and size_str.isnumeric():
        max_m_bytes = int(size_str)

    return max_m_bytes * 1024 * 1024


def get_backup_count() -> int:
    backup_cnt = 2
    cnt_str = os.getenv(LOG_BACKUP_COUNT, "2")
    if cnt_str is not None and cnt_str.isnumeric():
        backup_cnt = int(cnt_str)

    return backup_cnt


def check_log_file():
    create_flag = False
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR, exist_ok=True)
            log_file = Path(LOG_FILE)
            if not log_file.exists():
                log_file.touch()
        create_flag = True
    except IOError as e:
        print(e)
        print(f"log file create err!")
    finally:
        return create_flag


check_log_file()
