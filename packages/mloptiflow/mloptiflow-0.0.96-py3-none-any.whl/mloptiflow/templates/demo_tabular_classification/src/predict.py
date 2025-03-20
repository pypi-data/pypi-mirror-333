import logging
import logging.config
from typing import Optional, Any, Dict, Union, List
import numpy as np
import pandas as pd
import mlflow
from sklearn.datasets import load_breast_cancer
from mloptiflow.model_registry.registry import ModelRegistry
from mloptiflow.utils.exceptions import PredictionError

try:
    from logger.logger_config import LOGGING_CONFIG
except ImportError:
    from mloptiflow.templates.demo_tabular_classification.logger.logger_config import (
        LOGGING_CONFIG,
    )


logging.config.dictConfig(LOGGING_CONFIG)


class ModelPredictor:
    def __init__(
        self,
        experiment_name: str = "demo-tabular-classification",
        model_name: Optional[str] = None,
        tracking_uri: Optional[str] = None,
    ):
        self.registry = ModelRegistry(tracking_uri)
        self.experiment_name = experiment_name
        self.model_name = model_name or "XGBoost"
        self.model = None
        self.scaler = None
        self.feature_names = list(load_breast_cancer().feature_names)
        self._load_artifacts()

    def _load_artifacts(self):
        try:
            model_info = self.registry.get_latest_model(
                self.experiment_name, self.model_name
            )
            self.model = mlflow.sklearn.load_model(model_info["model_uri"])
            self.scaler = mlflow.sklearn.load_model(model_info["scaler_uri"])
        except Exception as e:
            raise PredictionError(f"Failed to load artifacts: {str(e)}") from e

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        try:
            if isinstance(X, np.ndarray):
                X = pd.DataFrame(X, columns=self.feature_names)

            X_scaled = self.scaler.transform(X)

            y_pred = self.model.predict(X_scaled)
            y_pred_proba = self.model.predict_proba(X_scaled)

            return {
                "predictions": y_pred,
                "probabilities": y_pred_proba,
                "prediction_classes": self.model.classes_,
            }
        except Exception as e:
            logging.error(f"Failed to make predictions: {str(e)}")
            raise PredictionError(f"Failed to make predictions: {str(e)}") from e

    def predict_single(
        self, features: Union[np.ndarray, List[float]]
    ) -> Dict[str, Any]:
        features_array = np.array(features).reshape(1, -1)
        result = self.predict(features_array)
        return {
            "prediction": result["predictions"][0],
            "probability": result["probabilities"][0],
            "prediction_classes": result["prediction_classes"],
        }


def main():
    try:
        predictor = ModelPredictor()
        example_features = load_breast_cancer().data[0]
        result = predictor.predict_single(example_features)

        print("\nPrediction Results:")
        print(f"Predicted Class: {result['prediction']}")
        print(f"Class Probabilities: {result['probability']}")
        print(f"Classes: {result['classes']}")

    except Exception as e:
        logging.error(f"Error in prediction pipeline: {str(e)}")
        raise


if __name__ == "__main__":
    main()
