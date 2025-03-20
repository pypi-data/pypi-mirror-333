import time
from .base_handler import (
    BaseClassificationInferenceHandler,
    BaseRegressionInferenceHandler,
    ClassificationInferenceData,
    RegressionInferenceData,
)
from typing import Dict, Any
import logging
import joblib
from sklearn.datasets import load_breast_cancer


class TabularClassificationInferenceHandler(BaseClassificationInferenceHandler):
    def serialize(self, data: ClassificationInferenceData) -> Dict:
        return {
            "features": data.features,
            "prediction": data.prediction,
            "probabilities": data.probabilities,
            "model_version": data.model_version,
            "timestamp": data.timestamp,
            "metadata": {
                "data_type": "tabular",
                "feature_names": self.handler.feature_names,
            },
        }


class TabularRegressionInferenceHandler(BaseRegressionInferenceHandler):
    def serialize(self, data: RegressionInferenceData) -> Dict:
        return {
            "features": data.features,
            "prediction": data.prediction,
            "model_version": data.model_version,
            "timestamp": data.timestamp,
            "metadata": {
                "data_type": "tabular",
                "feature_names": self.handler.feature_names,
            },
        }


class TabularClassificationMonitoringContext:
    def __init__(self, kafka_config: Dict):
        self.handler = TabularClassificationInferenceHandler(kafka_config)
        self._model_version = "0.0.1"
        self.feature_name = self._load_feature_names()

    def __enter__(self):
        self.handler.__enter__()
        return self

    def __exit__(self, *args):
        self.handler.__exit__(*args)

    def _load_feature_names(self):
        try:
            feature_metadata = joblib.load("out/models/feature_metadata.joblib")
            return feature_metadata["feature_names"]
        except Exception as e:
            logging.error(f"Error loading feature names: {e}")
            return list(load_breast_cancer().feature_names)

    def capture(self, features: list, prediction: Any, probabilities: list):
        data = ClassificationInferenceData(
            features=features,
            prediction=prediction,
            probabilities=probabilities,
            model_version=self._model_version,
            timestamp=int(time.time() * 1000),
            metadata={
                "data_type": "tabular",
                "feature_names": self.feature_name,
            },
        )
        self.handler.stream(data)


class TabularRegressionMonitoringContext:
    def __init__(self, kafka_config: Dict):
        self.handler = TabularRegressionInferenceHandler(kafka_config)
        self._model_version = "0.0.1"
        self.feature_name = self._load_feature_names()

    def __enter__(self):
        self.handler.__enter__()
        return self

    def _load_feature_names(self):
        try:
            feature_metadata = joblib.load("out/models/feature_metadata.joblib")
            return feature_metadata["feature_names"]
        except Exception as e:
            logging.error(f"Error loading feature names: {e}")
            raise e

    def __exit__(self, *args):
        self.handler.__exit__(*args)

    def capture(self, features: list, prediction: Any):
        data = RegressionInferenceData(
            features=features,
            prediction=prediction,
            model_version=self._model_version,
            timestamp=int(time.time() * 1000),
            metadata={
                "data_type": "tabular",
                "feature_names": self.feature_name,
            },
        )
        self.handler.stream(data)
