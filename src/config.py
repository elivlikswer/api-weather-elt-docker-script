import os
from dotenv import load_dotenv
from dataclasses import dataclass
import logging
from datetime import datetime

logger = logging.getLogger(__name__)



#data class
@dataclass
class AppConfig:
    latitude: float
    longitude: float
    url: str
    output_format: str
    start_date: str
    end_date: str
    hourly: list[str]
    timezone: str

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
        Loads params from .env: latitude, longitude, url, output_format
        :return: object of AppConfig.
        """
        try:
            latitude = os.getenv("LATITUDE")
            longitude = os.getenv("LONGITUDE")

            url = os.getenv("BASE_URL")

            output_format = os.getenv("OUTPUT_FORMAT","parquet")

            start_date = os.getenv("START_DATE")
            end_date = os.getenv("END_DATE")

            hourly_str = os.getenv("HOURLY")

            if hourly_str:
                hourly = hourly_str.split(",")
            else:
                hourly = ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m"]

            timezone = os.getenv("TIMEZONE")

            logger.info("Latitude: %s, Longitude: %s, URL: %s, Output format: %s, Start: %s, End: %s, Hourly: %s, Timezone: %s", latitude, longitude,url, output_format,start_date,end_date,hourly,timezone)

            self.appConfig = AppConfig(*self._check_for_attributes(latitude,longitude,url,output_format,start_date,end_date,hourly,timezone))

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



    def _check_for_attributes(self,latitude: str, longitude: str,url: str, output_format:str, start_date:str,end_date:str,hourly:list[str],timezone:str):
        """
        Validate params for empty
        :return: tuple of params
        """

        if not all([latitude, longitude, url, output_format, start_date, end_date, timezone]):
            raise ValueError("Missing required environment variables")

        if not hourly:
            raise ValueError("HOURLY must contain at least one parameter")

        try:
            lat_float = float(latitude)
            lon_float = float(longitude)

        except TypeError as e:
            logger.warning("Error on an attempt to float latitude and longitude. Error: %s. Latitude: %s, longitude: %s",type(e), longitude,longitude)
            raise e

        try:
            datetime.strptime(start_date,"%Y-%m-%d")
            datetime.strptime(end_date,"%Y-%m-%d")
        except ValueError as e:
            logger.warning("Invalid date format. Expected YYYY-MM-DD")
            raise e


        return (lat_float,lon_float,url,output_format,start_date,end_date,hourly,timezone)