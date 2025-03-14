import pytest
from raja_aita.api import api
from raja_aita.settings import Settings
from raja_aita.routers import get_settings


@pytest.fixture
def settings():
    return Settings(cleanup_username="username", cleanup_password="secret")


@pytest.fixture(autouse=True)
def inject_settings(settings):
    api.dependency_overrides[get_settings] = lambda: settings
