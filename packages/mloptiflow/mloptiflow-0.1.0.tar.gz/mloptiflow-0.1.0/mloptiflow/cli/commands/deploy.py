import click
import subprocess
import sys
import os
from pathlib import Path
import time
import threading
from mloptiflow.deployment.config import DeploymentConfig


@click.group()
def deploy():
    pass


def _run_api_tests(test_script: Path):
    if not test_script.exists():
        raise click.ClickException("API test script not found")
    subprocess.run([sys.executable, str(test_script)], check=True)


@deploy.command()
@click.option(
    "--target",
    type=click.Choice(["host-machine", "container"]),
    required=True,
    help="Deployment target: 'host-machine' for local deployment or 'container' to deploy inside a Docker container",
)
@click.option(
    "--kafka-monitoring",
    is_flag=True,
    help="(Only available when --target=container) Enable Kafka-based model monitoring",
)
@click.option(
    "--with-monitoring-ui",
    is_flag=True,
    help="(Requires --kafka-monitoring) Start the monitoring UI dashboard",
)
@click.option(
    "--ui-port",
    default=8501,
    type=int,
    help="Port for the monitoring UI (if enabled)",
)
@click.option("--host", default="0.0.0.0", help="Host to bind the API server")
@click.option("--port", default=8000, type=int, help="Port to bind the API server")
@click.option("--with-api-test", is_flag=True, help="Run inference API testing script")
def start(
    target: str,
    kafka_monitoring: bool,
    with_monitoring_ui: bool,
    ui_port: int,
    host: str,
    port: int,
    with_api_test: bool,
):
    config = DeploymentConfig(Path.cwd())
    cwd = Path.cwd()
    api_script = cwd / "app.py"
    api_test_script = cwd / "scripts" / "test_inference_api.py"

    if not api_script.exists():
        raise click.ClickException("app.py not found. Are you in the project root?")

    if target == "host-machine" and kafka_monitoring:
        raise click.ClickException(
            "--kafka-monitoring flag is only available when --target=container"
        )

    if with_monitoring_ui and not kafka_monitoring:
        raise click.ClickException(
            "--with-monitoring-ui requires --kafka-monitoring to be enabled"
        )

    if target == "host-machine":
        subprocess.Popen(
            [sys.executable, str(api_script)],
            env={**os.environ, "HOST": host, "PORT": str(port)},
        )
        click.echo(f"API server starting at http://{host}:{port}")
        if with_api_test:
            time.sleep(5)
            _run_api_tests(api_test_script)
    elif target == "container":
        config.enable_docker().setup()
        if kafka_monitoring:
            click.echo("Starting containerized deployment with Kafka...")
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    str(config.deployment_path / "docker-compose.yml"),
                    "up",
                    "-d",
                ],
                check=True,
            )

            if with_monitoring_ui:
                from mloptiflow.monitoring.config import MonitoringConfig
                from mloptiflow.monitoring.ui import start_monitoring_ui

                ui_config = MonitoringConfig()
                ui_config.enabled = True
                ui_config.kafka = {
                    "topic_name": "mloptiflow-inference-monitoring",
                    "bootstrap_servers": "localhost:9092",
                    "consumer_group": "mloptiflow-monitoring-ui",
                }

                click.echo(f"Starting monitoring UI at http://localhost:{ui_port}")
                click.echo("Connecting to Kafka at: localhost:9092")

                os.environ["KAFKA_BROKERS"] = "localhost:9092"
                os.environ["KAFKA_TOPIC"] = "mloptiflow-inference-monitoring"
                os.environ["KAFKA_CONSUMER_GROUP"] = "mloptiflow-monitoring-ui"

                click.echo("Waiting for Kafka to be ready...")
                time.sleep(10)

                ui_thread = threading.Thread(
                    target=start_monitoring_ui, args=(ui_config, ui_port), daemon=True
                )
                # ui_thread.start()

                time.sleep(2)

                click.echo(f"Monitoring UI is running at http://localhost:{ui_port}")
                click.echo(
                    "(The UI will automatically close when you exit this process)"
                )

        else:
            click.echo("Building API container image...")
            subprocess.run(
                [
                    "docker",
                    "build",
                    "-t",
                    "mloptiflow-api",
                    "-f",
                    str(config.deployment_path / "Dockerfile.api"),
                    ".",
                ],
                check=True,
            )

            docker_cmd = [
                "docker",
                "run",
                "-d",
                "-p",
                f"{port}:8000",
                "-v",
                f"{cwd}/mlruns:/app/mlruns",
                "-e",
                "MLFLOW_TRACKING_URI=file:///app/mlruns",
                "mloptiflow-api",
            ]

            click.echo("Starting standalone API container...")
            subprocess.run(docker_cmd, check=True)

        if with_api_test:
            time.sleep(5)
            _run_api_tests(api_test_script)
    else:
        raise click.ClickException("Invalid deployment target specified")

    if target == "container" and kafka_monitoring and with_monitoring_ui:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            click.echo("Stopping services...")
