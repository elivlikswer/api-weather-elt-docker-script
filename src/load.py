from pathlib import Path
import pandas as pd
root_dir = Path(__file__).parent.parent

import logging
logger = logging.getLogger(__name__)

class Load:
    def __init__(self, output_format:str ,base_dir=root_dir / "data"):
        self.base_dir = base_dir
        self.output_format = output_format

        base_dir.mkdir(parents=True,exist_ok=True)

        logger.info("Object class Load was successfully created")

    def save(self,df,start_date, end_date):
        try:
            file_name = f"weather_{start_date}_to_{end_date}.{self.output_format}"
            file_path = self.base_dir / file_name
            logger.info("file name was successfully created")

            if self.output_format.lower() == "csv":
                df.to_csv(
                    file_path,
                    index=False,
                    encoding="utf-8",
                    sep=",")

            elif self.output_format.lower() == "parquet":
                df.to_parquet(
                    self.base_dir / file_name,
                    engine="pyarrow",
                    compression='snappy',
                    index=False
                )

            else:
                logger.warning("Unsupported format: %s", self.output_format)
                return
            logger.info("Data successfully saved to %s", file_path)

        except Exception as e:
            logger.warning("Error at attempt to load DataFrame to local file: %s",e)
            raise