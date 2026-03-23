from common.common import setup_app_logging
setup_app_logging()

from extractor import Extractor
from config import Config
from transformer import Transform
from load import Load
import logging


logger = logging.getLogger(__name__)

config = Config()
appConfig = config.return_AppConfig()

extractor = Extractor(appConfig)
data = extractor.get_weather("2026-03-10","2026-03-17")

transformer = Transform(data)
df = transformer.dict_to_df()

start_date, end_date = transformer.fetch_date()

loader = Load(appConfig.output_format)
loader.save(df, start_date, end_date)