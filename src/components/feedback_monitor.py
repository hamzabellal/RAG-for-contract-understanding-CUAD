# src/components/feedback_monitor.py
import sys
from datetime import UTC, datetime, timedelta

import mlflow

from src.config.configuration import ConfigurationManager
from src.entity.config_entity import MonitoringConfig
from src.exception import CustomException
from src.logger import logging
from src.utils import get_db_connection


class FeedbackMonitor:
    def __init__(self, config: MonitoringConfig):
        self.monitoring_config = config

    def compute_like_ratio(self) -> dict:
        logging.info("computing like/dislike ratio from feedback")
        try:
            api_config = ConfigurationManager().get_api_config()
            conn = get_db_connection(api_config)
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT rating, COUNT(*) FROM feedback
                        WHERE timestamp >= %s
                        GROUP BY rating
                        """,
                        (datetime.now(UTC) - timedelta(days=self.monitoring_config.feedback_window_days),),
                    )
                    counts = dict(cur.fetchall())
            finally:
                conn.close()

            like_count = counts.get("like", 0)
            dislike_count = counts.get("dislike", 0)
            total = like_count + dislike_count
            like_ratio = like_count / total if total > 0 else None

            stats = {
                "like_count": like_count,
                "dislike_count": dislike_count,
                "total_feedback": total,
                "like_ratio": like_ratio,
            }
            logging.info(f"feedback stats over last {self.monitoring_config.feedback_window_days} days: {stats}")
            return stats
        except Exception as e:
            raise CustomException(e, sys)

    def log_to_mlflow(self, stats: dict):
        logging.info("logging feedback monitoring run to mlflow")
        try:
            mlflow.set_tracking_uri(self.monitoring_config.mlflow_tracking_uri)
            mlflow.set_experiment(self.monitoring_config.mlflow_experiment_name)

            with mlflow.start_run():
                mlflow.log_param("feedback_window_days", self.monitoring_config.feedback_window_days)
                mlflow.log_metric("like_count", stats["like_count"])
                mlflow.log_metric("dislike_count", stats["dislike_count"])
                mlflow.log_metric("total_feedback", stats["total_feedback"])
                if stats["like_ratio"] is not None:
                    mlflow.log_metric("like_ratio", stats["like_ratio"])
        except Exception as e:
            raise CustomException(e, sys)

    def run(self) -> dict:
        stats = self.compute_like_ratio()
        self.log_to_mlflow(stats)
        return stats
