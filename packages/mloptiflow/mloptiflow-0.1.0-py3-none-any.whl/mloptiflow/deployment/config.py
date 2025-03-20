from pathlib import Path
import shutil
import os


class DeploymentConfig:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.deployment_path = self.project_path / "deployment"
        self.with_monitoring = False
        self.with_docker = False

    def enable_monitoring(self):
        self.with_monitoring = True
        return self

    def enable_docker(self):
        self.with_docker = True
        return self

    def setup(self):
        if self.with_docker:
            self._copy_docker_files()

        if self.with_monitoring:
            os.environ["ENABLE_MONITORING"] = "true"

    def _copy_docker_files(self):
        template_path = (
            Path(__file__).parent.parent
            / "templates/demo_tabular_classification/deployment"
        )
        self.deployment_path.mkdir(exist_ok=True)

        for filename in ["Dockerfile.api", "Dockerfile.kafka", "docker-compose.yml"]:
            destination_file = self.deployment_path / filename
            if not destination_file.exists():
                shutil.copy2(template_path / filename, destination_file)
            else:
                print(f"Skipping copying {filename} as it already exists.")
