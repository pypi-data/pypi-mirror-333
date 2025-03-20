import pandas as pd
import plotly.express as px
import streamlit as st


def plot_feature_histogram(feature_name: str, feature_values: pd.Series):
    if feature_values.empty:
        st.write(f"No data available for {feature_name}")
        return

    fig = px.histogram(
        x=feature_values,
        title=f"Distribution of {feature_name}",
        labels={"x": feature_name, "y": "Count"},
        opacity=0.7,
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    stats = {
        "Mean": feature_values.mean(),
        "Median": feature_values.median(),
        "Std Dev": feature_values.std(),
        "Min": feature_values.min(),
        "Max": feature_values.max(),
    }
    st.write(stats)


def plot_prediction_histogram(predictions: pd.Series):
    if predictions.empty:
        st.write("No prediction data available")
        return

    fig = px.histogram(
        x=predictions,
        title="Distribution of Predictions",
        labels={"x": "Prediction", "y": "Count"},
        opacity=0.7,
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    stats = {
        "Mean": predictions.mean(),
        "Median": predictions.median(),
        "Std Dev": predictions.std(),
        "Min": predictions.min(),
        "Max": predictions.max(),
    }
    st.write(stats)


def plot_predictions_timeline(time_data: pd.DataFrame):
    if time_data.empty:
        st.write("No prediction timeline data available")
        return

    time_data = time_data.copy()
    time_data["datetime"] = pd.to_datetime(time_data["timestamp"], unit="ms")

    fig = px.line(
        time_data,
        x="datetime",
        y="prediction",
        title="Predictions Over Time",
        labels={"datetime": "Time", "prediction": "Prediction Value"},
    )
    st.plotly_chart(fig, use_container_width=True)
