from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from quixstreams import Application
from pydantic import BaseModel
from typing import Any, Dict
from tenacity import retry, wait_exponential, stop_after_attempt
import logging
from confluent_kafka.admin import AdminClient, NewTopic


class ClassificationInferenceData(BaseModel):
    features: list
    prediction: Any
    probabilities: list
    model_version: str
    timestamp: int


class RegressionInferenceData(BaseModel):
    features: list
    prediction: Any
    model_version: str
    timestamp: int


class BaseClassificationInferenceHandler(AbstractContextManager, ABC):
    def __init__(self, kafka_config: Dict[str, Any]):
        self._broker_address = kafka_config.get("bootstrap_servers", "localhost:9092")
        self._topic_name = kafka_config["topic_name"]
        self._consumer_group = kafka_config.get(
            "consumer_group", "mloptiflow-monitoring"
        )

        self._ensure_topic_exists()

        self._app = Application(
            broker_address=self._broker_address,
            consumer_group=self._consumer_group,
            auto_offset_reset="latest",
        )
        self._topic = self._app.topic(name=self._topic_name)
        self._producer = None

    def _ensure_topic_exists(self):
        try:
            logging.info(f"Ensuring Kafka topic '{self._topic_name}' exists...")
            admin_client = AdminClient({"bootstrap.servers": self._broker_address})

            metadata = admin_client.list_topics(timeout=10.0)
            if self._topic_name in metadata.topics:
                logging.info(f"Topic '{self._topic_name}' already exists")
                return

            topic_list = [
                NewTopic(self._topic_name, num_partitions=1, replication_factor=1)
            ]

            logging.info(f"Creating topic '{self._topic_name}'...")
            fs = admin_client.create_topics(topic_list)
            for topic, f in fs.items():
                try:
                    f.result()
                    logging.info(f"Topic '{topic}' created successfully")
                except Exception as e:
                    if "already exists" in str(e):
                        logging.info(f"Topic '{topic}' already exists")
                    else:
                        logging.error(f"Failed to create topic '{topic}': {e}")
        except Exception as e:
            logging.error(f"Error creating Kafka topic: {e}")

    def __enter__(self):
        self._producer = self._app.get_producer()
        return self

    def __exit__(self, *args):
        if self._producer:
            self._producer.close()

    @abstractmethod
    def serialize(self, data: ClassificationInferenceData) -> Dict:
        pass

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3)
    )
    def stream(self, data: ClassificationInferenceData):
        serialized = self.serialize(data)
        self._producer.produce(
            topic=self._topic.name,
            key=data.model_version,
            value=serialized,
        )


class BaseRegressionInferenceHandler(AbstractContextManager, ABC):
    def __init__(self, kafka_config: Dict[str, Any]):
        self._broker_address = kafka_config.get("bootstrap_servers", "localhost:9092")
        self._topic_name = kafka_config.get(
            "topic_name", "mloptiflow-inference-monitoring"
        )
        self._consumer_group = kafka_config.get(
            "consumer_group", "mloptiflow-monitoring"
        )

        self._ensure_topic_exists()

        self._app = Application(
            broker_address=self._broker_address,
            consumer_group=self._consumer_group,
            auto_offset_reset="latest",
        )
        self._topic = self._app.topic(name=self._topic_name)
        self._producer = None

    def _ensure_topic_exists(self):
        try:
            logging.info(f"Ensuring Kafka topic '{self._topic_name}' exists...")
            admin_client = AdminClient({"bootstrap.servers": self._broker_address})

            metadata = admin_client.list_topics(timeout=10.0)
            if self._topic_name in metadata.topics:
                logging.info(f"Topic '{self._topic_name}' already exists")
                return

            topic_list = [
                NewTopic(self._topic_name, num_partitions=1, replication_factor=1)
            ]

            logging.info(f"Creating topic '{self._topic_name}'...")
            fs = admin_client.create_topics(topic_list)
            for topic, f in fs.items():
                try:
                    f.result()
                    logging.info(f"Topic '{topic}' created successfully")
                except Exception as e:
                    if "already exists" in str(e):
                        logging.info(f"Topic '{topic}' already exists")
                    else:
                        logging.error(f"Failed to create topic '{topic}': {e}")
        except Exception as e:
            logging.error(f"Error creating Kafka topic: {e}")

    def __enter__(self):
        self._producer = self._app.get_producer()
        return self

    def __exit__(self, *args):
        if self._producer:
            self._producer.close()

    @abstractmethod
    def serialize(self, data: RegressionInferenceData) -> Dict:
        pass

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3)
    )
    def stream(self, data: RegressionInferenceData):
        serialized = self.serialize(data)
        self._producer.produce(
            topic=self._topic.name,
            key=data.model_version,
            value=serialized,
        )
