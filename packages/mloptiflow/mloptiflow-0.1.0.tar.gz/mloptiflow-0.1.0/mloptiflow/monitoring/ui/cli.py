import subprocess
import os
import sys
import threading
import webbrowser
import time
import importlib.util

from ..config import MonitoringConfig


def start_monitoring_ui(config: MonitoringConfig = None, port: int = 8501):
    if config is None:
        config = MonitoringConfig()

    module_spec = importlib.util.find_spec("mloptiflow.monitoring.ui.app")
    if module_spec is None:
        raise ImportError("Could not find mloptiflow.monitoring.ui.app module")

    app_path = module_spec.origin

    env = os.environ.copy()
    env["KAFKA_BROKERS"] = config.kafka["bootstrap_servers"]
    env["KAFKA_TOPIC"] = config.kafka["topic_name"]
    env["KAFKA_CONSUMER_GROUP"] = config.kafka["consumer_group"] + "-ui"

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.serverAddress",
        "localhost",
        "--theme.primaryColor",
        "#0066cc",
        "--theme.backgroundColor",
        "#ffffff",
        "--theme.secondaryBackgroundColor",
        "#f0f2f6",
        "--theme.textColor",
        "#262730",
    ]

    process = subprocess.Popen(cmd, env=env)

    def open_browser():
        time.sleep(2)
        webbrowser.open(f"http://localhost:{port}")

    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    print(f"Starting monitoring UI at http://localhost:{port}")
    print("Press Ctrl/^ + C to stop")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("Stopping monitoring UI...")
    finally:
        process.terminate()
