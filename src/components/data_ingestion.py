import sys

import pandas as pd
from datasets import concatenate_datasets, load_dataset

from src.entity.config_entity import DataIngestionConfig
from src.exception import CustomException
from src.logger import logging
from src.utils import clean_content


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.ingestion_config = config

    def extract_unique_contracts(self, data) -> list:
        logging.info("extracting unique contracts from the full dataset")
        try:
            seen_titles = set()
            unique_contracts = []
            for record in data:
                if record["title"] not in seen_titles:
                    seen_titles.add(record["title"])
                    unique_contracts.append({
                        "title" : record["title"],
                        "content" : record["context"]
                    })
            logging.info(f"extracted {len(unique_contracts)} unique contracts")
            return unique_contracts
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_ingestion(self):
        logging.info("starting data ingestion component")
        try:
            dataset = load_dataset(self.ingestion_config.data_source, revision="refs/convert/parquet")
            train_dataset = dataset["train"]
            test_dataset = dataset["test"]
            full_dataset = concatenate_datasets([train_dataset, test_dataset])
            full_dataset.to_json(self.ingestion_config.full_data_dir, orient="records", lines=True, compression="gzip")
            logging.info(f"full dataset saved at: {self.ingestion_config.full_data_dir}")

            unique_contracts = self.extract_unique_contracts(full_dataset)
            df_unique_contracts = pd.DataFrame(unique_contracts)
            df_unique_contracts.to_parquet(self.ingestion_config.contracts, index=False)
            logging.info(f"saved unique contracts at {self.ingestion_config.contracts}")

            df_unique_contracts["clean_content"] = df_unique_contracts["content"].apply(clean_content)
            df_unique_contracts.to_parquet(self.ingestion_config.cleaned_contracts, index=False)
            logging.info("content cleaning done succesfully and saved")

            content_len = df_unique_contracts["content"].str.len()
            clean_len = df_unique_contracts["clean_content"].str.len()
            reduction = (content_len - clean_len) / content_len * 100

            logging.info(f"average reduction in length after cleaning: {sum(reduction)/len(reduction):.1f}%")

            logging.info("contracts are ready to be chunked")

            return self.ingestion_config.cleaned_contracts
                         
        except Exception as e:
            raise CustomException(e, sys)