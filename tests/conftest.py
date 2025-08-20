import os
import sys
import pathlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def project_root():
    return pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def test_db_url(tmp_path_factory):
    db_dir = tmp_path_factory.mktemp("db")
    db_path = db_dir / "test.db"
    return f"sqlite+aiosqlite:///{db_path}"


@pytest.fixture(scope="session", autouse=True)
def setup_env(project_root, test_db_url):
    os.environ["POSTGRES_URL"] = test_db_url
    sys.path.insert(0, str(project_root))
    yield


@pytest.fixture(scope="session")
def app(setup_env):
    from main import app

    return app


@pytest.fixture()
def client(app):
    with TestClient(app) as c:
        yield c
