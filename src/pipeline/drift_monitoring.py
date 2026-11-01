import sys
from src.components.evaluation import Evaluator
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging
from src.pipeline.generation import GenerationPipeline

STAGE_NAME = "DRIFT MONITORING"

class DriftMonitoringPipeline:
    def __init__(self):
        pass
    def main(self):
        generator = GenerationPipeline().main()
        config = ConfigurationManager()
        monitoring_eval_config = config.get_monitoring_evaluation_config()
        evaluator = Evaluator(monitoring_eval_config, generator)
        return evaluator.run()


if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = DriftMonitoringPipeline()
        report = obj.main()
        logging.info(f"drift monitoring report: {report}")
        logging.info(f"stage {STAGE_NAME} completed\n\n")
    except Exception as e:
        raise CustomException(e, sys)