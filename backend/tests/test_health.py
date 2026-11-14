from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings, Settings


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_uses_centralized_settings():
    assert app.title == settings.app_name
    assert app.version == settings.app_version

def test_environment_variables_override_defaults(monkeypatch):
    monkeypatch.setenv("APP_NAME", "API de pruebas")
    monkeypatch.setenv("APP_VERSION", "9.9.9")

    test_settings = Settings(_env_file=None)

    assert test_settings.app_name == "API de pruebas"
    assert test_settings.app_version == "9.9.9"