import pandas as pd
import traceback
import logging

logger = logging.getLogger(__name__)



class Transform:
    def __init__(self, data: dict):
        self.data = data

    def dict_to_df(self):
        try:
            df = pd.DataFrame(self.data["hourly"])
            logger.info("API (json file) was successfully transformed into DataFrame")
            return df

        except KeyError as e:
            logger.error(f"Missing expected key in data: {e}")
            raise KeyError
        except Exception as e:
            logger.warning("Error at transform API (json file) to DataFrame. Type of error: %s",type(e))
            traceback.print_exc()
            raise Exception
