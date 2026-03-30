import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_app_logging(log_level=logging.INFO, log_dir="logfiles", log_file="app.log"):
    base_dir = Path(__file__).resolve().parent.parent.parent
    path = base_dir / log_dir
    path.mkdir(parents=True, exist_ok=True)
    log_path = path / log_file

    log_format = "[%(asctime)s] %(module)10s:%(lineno)3d %(levelname)-7s - %(message)s"

    # force=True сбросит все логгеры, которые могли успеть создаться при импортах
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            RotatingFileHandler(
                log_path,
                maxBytes=1024*1024,
                backupCount=5,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ],
        force=True
    )

    logging.info("--- Logger started ---")
    return True


