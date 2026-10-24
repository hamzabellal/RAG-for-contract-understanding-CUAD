import sys

from src.components.data_ingestion import DataIngestion
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging

STAGE_NAME = "DATA INGESTION"

class DataIngestionPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        clean_contracts = data_ingestion.initiate_data_ingestion()
        return clean_contracts

if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = DataIngestionPipeline()
        clean_contracts = obj.main()
        logging.info(f"stage {STAGE_NAME} completed\n")
    except Exception as e:
        raise CustomException(e, sys)
        