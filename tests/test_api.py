import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from uuid import uuid4
from zoneinfo import ZoneInfo

from raja_aita.api import api
from raja_aita.factories import RepositoryFactory
from raja_aita.models import Beacon


@pytest.fixture
def beacon():
    return Beacon(
        uid=uuid4(),
        dtstart=datetime(2024, 12, 23, 1, 2, 3, tzinfo=ZoneInfo("Europe/Berlin")),
        uptime=timedelta(hours=1),
    )


@pytest.fixture
def repository():
    return RepositoryFactory()()


@pytest.fixture(autouse=True)
def initialize_data(repository, beacon):
    repository.upsert_beacon(beacon)


@pytest.fixture
def client():
    return TestClient(api)


def test_get_beacons(client, beacon):
    response = client.get(f"/beacons/{beacon.uid}")

    assert response.status_code == 200
    assert response.json() == [beacon.model_dump(mode="json")]


def test_patch_beacons(repository, client, beacon):
    beacon.uptime = timedelta(hours=2)

    response = client.patch(
        f"/beacons/{beacon.uid}", json=beacon.model_dump(mode="json")
    )

    assert response.status_code == 200
    assert repository.find_beacons(beacon.uid) == [beacon]


def test_patch_beacons_with_unmatching_uid(client, beacon):
    response = client.patch(f"/beacons/{uuid4()}", json=beacon.model_dump(mode="json"))

    assert response.status_code == 403
