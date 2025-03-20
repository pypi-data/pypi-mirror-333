from typing import Dict, Any, List, Optional
import pandas as pd
from dataclasses import dataclass, field
import time


@dataclass
class MonitoringUIState:
    messages: List[Dict[str, Any]] = field(default_factory=list)
    feature_df: Optional[pd.DataFrame] = None
    prediction_df: Optional[pd.DataFrame] = None
    last_update: float = 0.0
    max_messages: int = 1000

    def update_from_messages(self, new_messages: List[Dict[str, Any]]):
        if not new_messages:
            return

        self.messages.extend(new_messages)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

        if self.messages:
            self._process_features()
            self._process_predictions()

        self.last_update = time.time()

    def _process_features(self):
        if not self.messages:
            return

        feature_data = []
        for msg in self.messages:
            if "features" not in msg or "metadata" not in msg:
                continue

            features = msg["features"]
            feature_names = msg.get("metadata", {}).get("feature_names", [])
            timestamp = msg.get("timestamp", int(time.time() * 1000))

            if not feature_names or len(feature_names) != len(features):
                feature_names = [f"feature_{i}" for i in range(len(features))]

            for i, value in enumerate(features):
                feature_data.append(
                    {"name": feature_names[i], "value": value, "timestamp": timestamp}
                )

        self.feature_df = pd.DataFrame(feature_data)

    def _process_predictions(self):
        if not self.messages:
            return

        prediction_data = []
        for msg in self.messages:
            if "prediction" not in msg:
                continue

            prediction = msg["prediction"]
            probabilities = msg.get("probabilities", [])
            timestamp = msg.get("timestamp", int(time.time() * 1000))

            prediction_data.append(
                {
                    "prediction": prediction,
                    "probabilities": probabilities,
                    "timestamp": timestamp,
                }
            )

        self.prediction_df = pd.DataFrame(prediction_data)

    def get_feature_distributions(self) -> Dict[str, pd.Series]:
        if self.feature_df is None or self.feature_df.empty:
            return {}

        return {name: group["value"] for name, group in self.feature_df.groupby("name")}

    def get_prediction_distribution(self) -> Optional[pd.Series]:
        if self.prediction_df is None or self.prediction_df.empty:
            return None

        return self.prediction_df["prediction"]

    def get_predictions_over_time(self) -> Optional[pd.DataFrame]:
        if self.prediction_df is None or self.prediction_df.empty:
            return None

        return self.prediction_df[["prediction", "timestamp"]].sort_values("timestamp")
