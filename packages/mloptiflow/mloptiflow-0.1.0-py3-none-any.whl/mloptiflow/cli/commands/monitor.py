import click


@click.group()
def monitor():
    pass


@monitor.command()
@click.option("--model-name", required=True, help="Name of deployed model to monitor")
@click.option(
    "--kafka-topic",
    default="mloptiflow-inference-monitoring",
    help="Kafka topic for monitoring data",
)
@click.option(
    "--bootstrap-servers", default="localhost:9092", help="Kafka bootstrap servers"
)
@click.option(
    "--prediction-type",
    type=click.Choice(["classification", "regression"]),
    required=True,
    help="Type of model predictions",
)
def start(
    model_name: str, kafka_topic: str, bootstrap_servers: str, prediction_type: str
):
    from mloptiflow.monitoring.consumer.service import start_monitoring
    import joblib

    try:
        training_stats = joblib.load("out/models/training_stats.joblib")

        click.echo(f"Starting monitoring for {model_name} ({prediction_type})")
        click.echo(f"Kafka config - Topic: {kafka_topic}, Servers: {bootstrap_servers}")

        start_monitoring(
            training_stats=training_stats,
            kafka_config={
                "topic_name": kafka_topic,
                "bootstrap_servers": bootstrap_servers,
                "prediction_type": prediction_type,
            },
        )
    except FileNotFoundError:
        click.echo("Error: Training statistics not found. Run training first.")
    except Exception as e:
        click.echo(f"Failed to start monitoring: {str(e)}")
