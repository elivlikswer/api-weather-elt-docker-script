import requests
import logging
from tenacity import (
retry,
stop_after_attempt,
wait_exponential,
retry_if_exception_type,
before_sleep_log
)

logger = logging.getLogger(__name__)


class Extractor:
    def __init__(self,forecast):
        self.url = forecast.url
        self.lat = forecast.latitude
        self.lon = forecast.longitude

    def get_weather(self,start_date: str, end_date: str):

        params = self.get_params(start_date, end_date)

        try:
            data = self._fetch_with_retry(params)
            return data

        except requests.exceptions.RequestException as e:
            logger.info("Network error wile fetching weather API. Error %s:",e)
            raise


    def get_params(self, start_date: str, end_date: str):
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m"],
            "timezone": "UTC"
        }
        return params

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(
            multiplier=0.1,
            min=0.1,
            max=5
        ),
        retry=retry_if_exception_type(
            requests.exceptions.RequestException
        ),
        before_sleep=before_sleep_log(logger,logging.WARNING) # type: ignore
    )
    def _fetch_with_retry(self, params):
        response = requests.get(self.url, params=params, timeout=10)
        # timeout - ограничивает время ожидания ответа от сервера, в данном случае на 10 секунд, чтобы не ждать ответа от сервиса вечно.

        response.raise_for_status()
        # raise_for_status нужно, в случае если  API ответит 4xx или 5xx, это вызовет исключение

        return response.json()