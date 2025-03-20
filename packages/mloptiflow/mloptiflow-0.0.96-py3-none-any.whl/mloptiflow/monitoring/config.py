from typing import Dict, Any
import os


class MonitoringConfig:
    def __init__(self):
        self.enabled = os.getenv("ENABLE_MONITORING", "false").lower() == "true"
        self.kafka = {
            "topic_name": os.getenv("KAFKA_TOPIC", "mloptiflow-inference-monitoring"),
            "bootstrap_servers": os.getenv("KAFKA_BROKERS", "localhost:9092"),
            "consumer_group": os.getenv(
                "KAFKA_CONSUMER_GROUP", "mloptiflow-monitoring"
            ),
        }

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "MonitoringConfig":
        instance = cls()
        instance.enabled = config.get("enabled", False)
        instance.kafka.update(config.get("kafka", {}))
        return instance


DEFAULT_CONFIG = MonitoringConfig()
