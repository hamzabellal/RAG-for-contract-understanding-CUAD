import sys

from src.components.feedback_monitor import FeedbackMonitor
from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging

STAGE_NAME = "FEEDBACK MONITORING"

class FeedbackMonitorPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        monitor_config = config.get_monitoring_config()
        monitor = FeedbackMonitor(monitor_config)
        return monitor.run()


if __name__ == "__main__":
    try:
        logging.info(f"stage {STAGE_NAME} started")
        obj = FeedbackMonitorPipeline()
        stats = obj.main()
        logging.info(f"feedback monitoring stats : {stats}")
        logging.info(f"stage {STAGE_NAME} completed\n\n")
    except Exception as e:
        raise CustomException(e, sys)