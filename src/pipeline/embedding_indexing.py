import sys

from src.components.embedding_indexing import EmbeddingIndexing
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging

STAGE_NAME = "EMBEDDING & INDEXING"

class EmbeddingIndexingPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        embedding_indexing_config = config.get_embedding_config()
        embedding_indexing = EmbeddingIndexing(embedding_indexing_config)
        report = embedding_indexing.initiate_embedding_indexing()
        return report


if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = EmbeddingIndexingPipeline()
        report = obj.main()
        logging.info(f"stage {STAGE_NAME} completed")
    except Exception as e:
        raise CustomException(e, sys)