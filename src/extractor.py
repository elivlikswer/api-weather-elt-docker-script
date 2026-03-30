from config import AppConfig
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
    def __init__(self,forecast:AppConfig):
        self.forecast = forecast

    def get_weather(self):

        params = self.get_params()

        try:
            data = self._fetch_with_retry(params)
            return data

        except requests.exceptions.RequestException as e:
            logger.info("Network error wile fetching weather API. Error %s:",e)
            raise


    def get_params(self):
        params = {
            "latitude": self.forecast.latitude,
            "longitude": self.forecast.longitude,
            "start_date": self.forecast.start_date,
            "end_date": self.forecast.end_date,
            "hourly": self.forecast.hourly,
            "timezone": self.forecast.timezone
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
        response = requests.get(self.forecast.url, params=params, timeout=10)
        # timeout - ограничивает время ожидания ответа от сервера, в данном случае на 10 секунд, чтобы не ждать ответа от сервиса вечно.

        response.raise_for_status()
        # raise_for_status нужно, в случае если  API ответит 4xx или 5xx, это вызовет исключение

        return response.json()