import sys

from src.components.evaluation import Evaluator
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging

STAGE_NAME = "EVAL SAMPLES"

class EvalSamplesPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        evaluation_config = config.get_evaluation_config()
        evaluator = Evaluator(evaluation_config)
        pos_samples, neg_samples = evaluator.build_eval_samples()
        return pos_samples, neg_samples

if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = EvalSamplesPipeline()
        pos_samples, neg_samples = obj.main()
        logging.info(f"evaluation samples built and saved : {len(pos_samples)} positive, {len(neg_samples)} negative")
        logging.info(f"stage {STAGE_NAME} completed\n")
    except Exception as e:
        raise CustomException(e, sys)