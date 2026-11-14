import sys
from pathlib import Path

from src.components.generation import Generator
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging
from src.pipeline.retrieval import RetrievalPipeline

STAGE_NAME = "GENERATION"

class GenerationPipeline:
    def __init__(self):
        pass
    def main(self):
        retrieval = RetrievalPipeline().main()
        config = ConfigurationManager()
        generation_config = config.get_generation_config()
        generator = Generator(generation_config, retrieval)
        generator.initiate_generation()
        return generator

if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = GenerationPipeline()
        generator = obj.main()
        
        items = [
            {
                "title": "ADUROBIOTECH,INC_06_02_2020-EX-10.7-CONSULTING AGREEMENT",
                "question": 'Highlight the parts (if any) of this contract related to \"Agreement Date\" that should be reviewed by a lawyer. Details: The date of the contract'
            },
            {
                "title": "ADUROBIOTECH,INC_06_02_2020-EX-10.7-CONSULTING AGREEMENT",
                "question": 'Highlight the parts (if any) of this contract related to \"Termination\" that should be reviewed by a lawyer. Details: The termination clause of the contract'
            }
        ]
        output_path = Path("artifacts/generation/generation_results.json")
        results = generator.run_batch(items, output_path)
        logging.info(f"test: {results}")

        logging.info(f"stage {STAGE_NAME} completed")
    except Exception as e:
        raise CustomException(e, sys)
