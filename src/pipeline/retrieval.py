import sys

from src.components.retrieval import Retrieval
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging

STAGE_NAME = "RETRIEVAL & RERANKING"

class RetrievalPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        retrieval_config = config.get_retrieval_config()
        retrieval = Retrieval(retrieval_config)
        retrieval.initiate_retrieval()
        return retrieval
    
if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = RetrievalPipeline()
        retriever = obj.main()

        chunks = retriever.retrieve(
            'Highlight the parts (if any) of this contract related to \"Agreement Date\" that should be reviewed by a lawyer. Details: The date of the contract',
            "ADUROBIOTECH,INC_06_02_2020-EX-10.7-CONSULTING AGREEMENT"
        )
        logging.info(f"test: {chunks}")

        logging.info(f"stage {STAGE_NAME} completed")
    except Exception as e:
        raise CustomException(e, sys)
