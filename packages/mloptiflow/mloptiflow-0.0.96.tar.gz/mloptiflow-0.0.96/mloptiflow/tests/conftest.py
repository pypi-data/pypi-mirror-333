import pytest
from pathlib import Path
import shutil
import tempfile


@pytest.fixture
def temp_dir():
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)
