from typing import Dict, Any, List
import json
import threading
import time
import os
from queue import Queue
from confluent_kafka import Consumer, KafkaException


class UIKafkaConsumer:
    def __init__(self, kafka_config: Dict[str, Any], max_messages: int = 1000):
        bootstrap_servers = os.environ.get("KAFKA_BROKERS")
        if not bootstrap_servers:
            bootstrap_servers = kafka_config.get("bootstrap_servers", "localhost:9092")

        topic = os.environ.get("KAFKA_TOPIC")
        if not topic:
            topic = kafka_config.get("topic_name", "mloptiflow-inference-monitoring")

        consumer_group = os.environ.get("KAFKA_CONSUMER_GROUP")
        if not consumer_group:
            consumer_group = kafka_config.get("consumer_group", "mloptiflow-ui")

        print(f"Connecting to Kafka broker: {bootstrap_servers}")
        print(f"Consuming from topic: {topic}")
        print(f"Using consumer group: {consumer_group}")

        self.config = {
            "bootstrap.servers": bootstrap_servers,
            "group.id": consumer_group,
            "auto.offset.reset": "latest",
            "enable.auto.commit": True,
            "client.id": "mloptiflow-ui-consumer",
            "socket.timeout.ms": 10000,
            "socket.keepalive.enable": True,
        }
        self.topic = topic
        self.max_messages = max_messages
        self.message_queue = Queue(maxsize=max_messages)
        self.should_run = False
        self.consumer_thread = None

    def start(self):
        if self.consumer_thread is not None and self.consumer_thread.is_alive():
            return

        self.should_run = True
        self.consumer_thread = threading.Thread(target=self._consume_loop)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

    def stop(self):
        self.should_run = False
        if self.consumer_thread is not None:
            self.consumer_thread.join(timeout=5.0)

    def _consume_loop(self):
        print(f"Starting Kafka consumer with config: {self.config}")
        try:
            consumer = Consumer(self.config)
            consumer.subscribe([self.topic])

            print("Successfully created consumer and subscribed to topic")

            try:
                metadata = consumer.list_topics(timeout=10.0)

                if (
                    "bootstrap.servers" in self.config
                    and "localhost" in self.config["bootstrap.servers"]
                ):
                    for broker_id, broker in metadata.brokers.items():
                        if broker.host == "kafka":
                            print(
                                f"Found broker advertising as {broker.host}:{broker.port}, will use localhost:{broker.port} instead"
                            )
            except Exception as e:
                print(f"Error listing topics: {e}")

            error_count = 0

            while self.should_run:
                try:
                    msg = consumer.poll(1.0)

                    if msg is None:
                        continue

                    if msg.error():
                        error_str = str(msg.error())
                        if "Failed to resolve 'kafka:9092'" in error_str:
                            if error_count % 10 == 0:
                                print(
                                    "Ignoring Kafka hostname resolution error - this is expected"
                                )
                            error_count += 1
                        else:
                            print("")
                        continue

                    error_count = 0

                    value = json.loads(msg.value().decode("utf-8"))
                    print(f"Received message: {value}")

                    if self.message_queue.full():
                        self.message_queue.get()

                    self.message_queue.put(value)
                except Exception as e:
                    print(f"Error processing message: {e}")
                    time.sleep(0.5)

        except KafkaException as e:
            print(f"Kafka exception: {e}")
        except Exception as e:
            print(f"Unexpected error in consumer loop: {e}")
        finally:
            try:
                consumer.close()
            except:
                pass

    def get_messages(self) -> List[Dict[str, Any]]:
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages
