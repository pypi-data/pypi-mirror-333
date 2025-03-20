from quixstreams import Application
import pandas as pd
from typing import Dict, Any
from pydantic import BaseModel, ValidationError
import logging
import mlflow
import time
from scipy.stats import entropy
import numpy as np


class ClassificationInferenceMessage(BaseModel):
    features: list
    prediction: float
    probabilities: list
    model_version: str
    timestamp: int
    metadata: dict


class RegressionInferenceMessage(BaseModel):
    features: list
    prediction: float
    model_version: str
    timestamp: int
    metadata: dict


class DriftDetector:
    def __init__(self, training_stats: Dict[str, Any], kafka_config: Dict[str, Any]):
        self._training_stats = training_stats
        self._app = Application.Quix(
            consumer_group="mloptiflow-drift-detector",
            auto_offset_reset="earliest",
            auto_create_topics=True,
            broker_address=kafka_config.get("bootstrap_servers", "localhost:9092"),
        )
        self._topic = self._app.topic(
            kafka_config["topic_name"],
            config={
                "bootstrap.servers": kafka_config.get(
                    "bootstrap_servers", "localhost:9092"
                )
            },
        )
        self._inference_message_cls = (
            ClassificationInferenceMessage
            if kafka_config["prediction_type"] == "classification"
            else RegressionInferenceMessage
        )

    def _calculate_kl_divergence(
        self, train_stats: Dict[str, float], inference_samples: pd.Series
    ):
        bin_edges = np.linspace(
            train_stats["min"] - 0.1 * (train_stats["max"] - train_stats["min"]),
            train_stats["max"] + 0.1 * (train_stats["max"] - train_stats["min"]),
            num=20,
        )
        train_hist, _ = np.histogram(
            np.random.normal(
                loc=train_stats["mean"], scale=train_stats["std"], size=1000
            ),
            bins=bin_edges,
            density=True,
        )
        inf_hist, _ = np.histogram(inference_samples, bins=bin_edges, density=True)
        train_hist = np.clip(train_hist, 1e-9, None)
        inf_hist = np.clip(inf_hist, 1e-9, None)
        return entropy(train_hist, inf_hist)

    def _detect_drift(self, features: pd.DataFrame):
        return {
            feature: self._calculate_kl_divergence(
                self._training_stats[feature], features[feature]
            )
            for feature in features.columns
        }

    def start(self):
        with self._app.get_consumer() as consumer:
            for msg in consumer:
                try:
                    validated = self._inference_message_cls(**msg.value)
                    features_df = pd.DataFrame(
                        [validated.features],
                        columns=validated.metadata["feature_names"],
                    )
                    drift_scores = self._detect_drift(features_df)
                    self._log_drift(drift_scores, validated.model_version)
                except ValidationError as e:
                    logging.error(f"Invalid message format: {e}")

    def _log_drift(self, scores: Dict[str, float], model_version: str):
        with mlflow.start_run(run_name=f"drift-{int(time.time())}"):
            mlflow.log_metrics(scores)
            mlflow.log_param("model_version", model_version)
