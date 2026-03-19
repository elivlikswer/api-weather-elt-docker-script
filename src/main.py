from extractor import Extractor
from api_object import Forecast
from config import Config

import logging
logger = logging.getLogger(__name__)

config = Config()
forecast = Forecast(config)
extractor = Extractor(forecast)

print(extractor.get_weather("2026-03-10","2026-03-17"))