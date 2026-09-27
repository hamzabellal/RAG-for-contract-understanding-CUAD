from src.logger import logging
from src.exception import CustomException
from src.components.chunking import Chunker
from src.config.configuration import ConfigurationManager
import sys

STAGE_NAME = "CHUNKING"

class ChunkingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        chunking_config = config.get_chunking_config()
        chunker = Chunker(chunking_config)
        nodes_path = chunker.initiate_chunking()
        return nodes_path

if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = ChunkingPipeline()
        nodes_path = obj.main()
        logging.info(f"stage {STAGE_NAME} completed\n")
    except Exception as e:
        raise CustomException(e, sys)