import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
# def config_logging(level=logging.WARNING):
#     logging.basicConfig(level=level,
#                         datefmt='%Y-%m-%d %H:%M:%S',
#                         format='[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)3d %(levelname)-7s - %(message)s')

def setup_app_logging(log_level=logging.INFO,log_dir="logfiles",log_file="app.log"):

    base_dir = Path(__file__).resolve().parent.parent.parent

    path = base_dir / log_dir

    path.mkdir(parents=True, exist_ok=True)

    log_path = path / log_file

    print(f"DEBUG: Full log path: {log_path.absolute()}")

    log_format = logging.Formatter("[%(asctime)s] %(module)10s:%(lineno)3d %(levelname)-7s - %(message)s")


    file_handler = RotatingFileHandler(
        path / log_file,
        maxBytes=5*1024*1024,
        backupCount=5,
        encoding="utf-8")
    file_handler.setFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    root_logger.handlers = []


    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("--- Logger started ---")

    return True


