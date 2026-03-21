from common.common import setup_app_logging
setup_app_logging()

from extractor import Extractor
from config import Config
import logging


logger = logging.getLogger(__name__)

config = Config()
forecast = config.return_AppConfig()
extractor = Extractor(forecast)

print(extractor.get_weather("2026-03-10","2026-03-17"))