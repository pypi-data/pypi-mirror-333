import streamlit as st
import time
from typing import Dict, Any
import os

try:
    from .consumers import UIKafkaConsumer
    from .state import MonitoringUIState
    from .visualizations import (
        plot_feature_histogram,
        plot_prediction_histogram,
        plot_predictions_timeline,
    )
except ImportError:
    from mloptiflow.monitoring.ui.consumers import UIKafkaConsumer
    from mloptiflow.monitoring.ui.state import MonitoringUIState
    from mloptiflow.monitoring.ui.visualizations import (
        plot_feature_histogram,
        plot_prediction_histogram,
        plot_predictions_timeline,
    )


def run_monitoring_ui(kafka_config: Dict[str, Any], refresh_interval: int = 5):
    st.set_page_config(
        page_title="MLOPTIFLOW Monitoring",
        page_icon="📊",
        layout="wide",
    )

    if "state" not in st.session_state:
        st.session_state.state = MonitoringUIState()

    st.sidebar.title("Connection Info")
    st.sidebar.write(
        f"Kafka: {kafka_config.get('bootstrap_servers', 'localhost:9092')}"
    )
    st.sidebar.write(
        f"Topic: {kafka_config.get('topic_name', 'mloptiflow-inference-monitoring')}"
    )

    if "consumer" not in st.session_state:
        if "consumer" in st.session_state and st.session_state.consumer:
            st.session_state.consumer.stop()

        st.session_state.consumer = UIKafkaConsumer(kafka_config)

        st.session_state.consumer.start()

    st.title("MLOPTIFLOW Model Monitoring")
    st.markdown(
        """
        This dashboard shows real-time monitoring data from your deployed ML model.
    """
    )

    messages = st.session_state.consumer.get_messages()
    st.session_state.state.update_from_messages(messages)

    if not messages and st.session_state.state.last_update == 0:
        st.warning(
            "Waiting for data from Kafka... If this persists, check your Kafka connection."
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages Processed", len(st.session_state.state.messages))
    with col2:
        if st.session_state.state.last_update > 0:
            last_update_time = time.strftime(
                "%H:%M:%S", time.localtime(st.session_state.state.last_update)
            )
            st.metric("Last Update", last_update_time)

    if st.button("Refresh Data"):
        messages = st.session_state.consumer.get_messages()
        st.session_state.state.update_from_messages(messages)
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["Features", "Predictions", "Timeline"])

    with tab1:
        st.header("Feature Distributions")
        feature_distributions = st.session_state.state.get_feature_distributions()

        if not feature_distributions:
            st.info("No feature data available yet.")
        else:
            feature_names = list(feature_distributions.keys())
            selected_features = st.multiselect(
                "Select features to display",
                options=feature_names,
                default=feature_names[: min(3, len(feature_names))],
            )

            if selected_features:
                feature_cols = st.columns(min(3, len(selected_features)))
                for i, feature_name in enumerate(selected_features):
                    with feature_cols[i % len(feature_cols)]:
                        plot_feature_histogram(
                            feature_name, feature_distributions[feature_name]
                        )
            else:
                st.info("Please select at least one feature to display.")

    with tab2:
        st.header("Prediction Distribution")
        predictions = st.session_state.state.get_prediction_distribution()

        if predictions is None or predictions.empty:
            st.info("No prediction data available yet.")
        else:
            plot_prediction_histogram(predictions)

    with tab3:
        st.header("Predictions Over Time")
        time_data = st.session_state.state.get_predictions_over_time()

        if time_data is None or time_data.empty:
            st.info("No timeline data available yet.")
        else:
            plot_predictions_timeline(time_data)

    time.sleep(refresh_interval)
    st.rerun()


def main():
    kafka_config = {
        "bootstrap_servers": os.environ.get("KAFKA_BROKERS", "localhost:9092"),
        "topic_name": os.environ.get("KAFKA_TOPIC", "mloptiflow-inference-monitoring"),
        "consumer_group": os.environ.get("KAFKA_CONSUMER_GROUP", "mloptiflow-ui"),
    }

    run_monitoring_ui(kafka_config)


if __name__ == "__main__":
    main()
