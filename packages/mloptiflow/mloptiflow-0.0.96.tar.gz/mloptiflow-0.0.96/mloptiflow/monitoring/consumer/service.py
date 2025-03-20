from .drift_detector import DriftDetector
import logging
from typing import Dict, Any


def start_monitoring(training_stats: Dict[str, Any], kafka_config: Dict[str, Any]):
    logging.basicConfig(level=logging.INFO)

    detector = DriftDetector(
        training_stats=training_stats,
        kafka_config=kafka_config,
    )

    logging.info("Starting drift monitoring consumer...")
    detector.start()


if __name__ == "__main__":
    start_monitoring()
