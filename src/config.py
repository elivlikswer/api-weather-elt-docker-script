import os
from dotenv import load_dotenv
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)



#data class
@dataclass
class AppConfig:
    latitude: float
    longitude: float
    url: str


#class config
class Config:
    def __init__(self):
        load_dotenv()
        self.isParams =  self._load_config_from_env()

    def return_AppConfig(self) -> AppConfig:
        """
        if all params are valid - returns object's class AppConfig
        :return: AppConfig
        """
        if self.isParams:
            return self.appConfig
        else:
            raise ValueError("Params in .env is not correct. Please check you env file.")

    def _load_config_from_env(self):
        """
        Loads params from .env: latitude, longitude, url
        :return: object of AppConfig.
        """
        try:
            latitude = os.getenv("LATITUDE")
            longitude = os.getenv("LONGITUDE")
            url = os.getenv("BASE_URL")
            logger.info("Latitude: %s, Longitude: %s, URL: %s", latitude, longitude,url)

            self.appConfig = AppConfig(*self._check_for_attributes(latitude,longitude,url))

            logger.info("The object class was successfully created.")
            return True

        except ValueError as e:
            logger.warning('Could not load environment variables. Error: %s',e)
            raise

        except KeyError as e:
            logger.warning('Could not load environment variables. Error: %s',e)
            raise

        except (ValueError, TypeError) as e:
            logger.warning("Error on an attempt to float latitude and longitude. Error: %s.",type(e))
            raise



    def _check_for_attributes(self,latitude: str, longitude: str,url: str):
        """
        Validate params for empty
        :return: tuple of params
        """

        if not all([latitude,longitude,url]):
            raise

        try:
            lat_float = float(latitude)
            lon_float = float(longitude)

        except (ValueError, TypeError) as e:
            logger.warning("Error on an attempt to float latitude and longitude. Error: %s. Latitude: %s, longitude: %s",type(e), longitude,longitude)
            raise e

        return (lat_float,lon_float,url)