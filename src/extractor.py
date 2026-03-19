import requests
import logging
from common.common import config_logging

logger = logging.getLogger('__name__')
config_logging(level=logging.INFO)

class Extractor:
    def __init__(self,forecast):
        self.url = forecast.url
        self.lat = forecast.latitude
        self.lon = forecast.longitude

    def get_weather(self,start_date: str, end_date: str):

        params = {
            "latitude":self.lat,
            "longitude":self.lon,
            "start_date":start_date,
            "end_date":end_date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m"],
            "timezone": "UTC"
        }

        try:
            response = requests.get(self.url,params=params,timeout=10)
            # timeout - ограничивает время ожидания ответа от сервера, в данном случае на 10 секунд, чтобы не ждать ответа от сервиса вечно.

            response.raise_for_status()

            # raise_for_status нужно, в случае если  API ответит 4xx или 5xx, это вызовет исключение

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.info("Network error wile fetching weather API. Error %s:",e)
            raise