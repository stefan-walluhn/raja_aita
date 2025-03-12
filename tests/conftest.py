import pytest
from raja_aita.config import Settings, get_settings
from raja_aita.api import api


@pytest.fixture
def settings():
    return Settings(cleanup_username="username", cleanup_password="secret")


@pytest.fixture(autouse=True)
def inject_settings(settings):
    api.dependency_overrides[get_settings] = lambda: settings
