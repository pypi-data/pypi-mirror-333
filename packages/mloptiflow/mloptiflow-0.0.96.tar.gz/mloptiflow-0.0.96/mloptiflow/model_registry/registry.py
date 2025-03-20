from typing import Optional, Dict, Any
import os
import mlflow
from mlflow.tracking import MlflowClient
from mloptiflow.utils.exceptions import PredictionError


class ModelRegistry:
    def __init__(self, tracking_uri: Optional[str] = None):
        self.tracking_uri = tracking_uri or "file:./mlruns"
        mlflow.set_tracking_uri(self.tracking_uri)
        self.client = MlflowClient()

    def get_latest_model(
        self, experiment_name: str, model_name: str = "XGBoost"
    ) -> Dict[str, Any]:
        experiment = self.client.get_experiment_by_name(experiment_name)
        if experiment is None:
            raise PredictionError(f"No experiment found with name: {experiment_name}")

        runs = self.client.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string="status = 'FINISHED'",
            order_by=["start_time DESC"],
            max_results=1,
        )

        if not runs:
            raise PredictionError("No successful runs found")

        run = runs[0]
        artifact_root = os.getenv("MLOPTIFLOW_ARTIFACT_ROOT")
        if artifact_root:
            model_uri = f"file://{artifact_root}/{experiment.experiment_id}/{run.info.run_id}/artifacts/{model_name}_model"
            scaler_uri = f"file://{artifact_root}/{experiment.experiment_id}/{run.info.run_id}/artifacts/scaler"
        else:
            model_uri = f"runs:/{run.info.run_id}/{model_name}_model"
            scaler_uri = f"runs:/{run.info.run_id}/scaler"

        return {
            "run_id": run.info.run_id,
            "model_uri": model_uri,
            "scaler_uri": scaler_uri,
        }

    def load_model(
        self, experiment_name: str, model_name: str = "XGBoost"
    ) -> Dict[str, Any]:
        model_info = self.get_latest_model(experiment_name, model_name)
        return {
            "model": mlflow.sklearn.load_model(model_info["model_uri"]),
            "scaler": mlflow.sklearn.load_model(model_info["scaler_uri"]),
        }
