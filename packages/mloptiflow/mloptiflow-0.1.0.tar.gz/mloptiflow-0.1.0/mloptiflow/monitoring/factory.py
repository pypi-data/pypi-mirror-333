from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from .config import MonitoringConfig
from .producer.tabular_handler import TabularClassificationMonitoringContext


class MonitoringBackend(ABC):
    @abstractmethod
    def capture(self, features: list, prediction: Any, probabilities: list):
        pass


class KafkaMonitoring(MonitoringBackend):
    def __init__(self, config: Dict[str, Any]):
        self.context = TabularClassificationMonitoringContext(config)

    def capture(self, features: list, prediction: Any, probabilities: list):
        with self.context as monitor:
            monitor.capture(features, prediction, probabilities)


class NoOpMonitoring(MonitoringBackend):
    def capture(self, features: list, prediction: Any, probabilities: list):
        logging.debug("Monitoring disabled - skipping capture")
        pass


def create_monitoring_backend(config: MonitoringConfig = None) -> MonitoringBackend:
    if config is None:
        config = MonitoringConfig()

    if not config.enabled:
        return NoOpMonitoring()
    return KafkaMonitoring(config.kafka)
