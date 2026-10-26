from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from backend.app import create_app


@pytest.fixture
def client(tmp_path: Path):
    app = create_app(database_path=str(tmp_path / 'test.db'), seed=False, read_only=False)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def read_only_client(tmp_path: Path):
    app = create_app(database_path=str(tmp_path / 'public-demo.db'), seed=True, read_only=True)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def example():
    return {'outlet': 'Demo Radio', 'channel': 'radio', 'status': 'planned',
            'due_date': '2026-11-05', 'notes': 'Synthetic example only'}
