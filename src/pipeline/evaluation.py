import sys

from src.components.evaluation import Evaluator
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging
from src.pipeline.generation import GenerationPipeline

STAGE_NAME = "EVALUATION"

class EvaluationPipeline:
    def __init__(self):
        pass
    def main(self):
        generator = GenerationPipeline().main()
        config = ConfigurationManager()
        evaluation_config = config.get_evaluation_config()
        evaluator = Evaluator(evaluation_config, generator)
        return evaluator

if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = EvaluationPipeline()
        evaluator = obj.main()
        report = evaluator.run()
        logging.info(f"stage {STAGE_NAME} completed\n\n")
    except Exception as e:
        raise CustomException(e, sys)
