import pytest
from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.testclient import TestClient
from uuid import UUID

from raja_aita.api import api
from raja_aita.models import Beacon
from raja_aita.routers import get_repository


@pytest.fixture
def uid():
    return "ac147910-29cd-4c7a-aadc-41e6f93bbf2b"


@pytest.fixture
def beacon(uid):
    return Beacon(
        uid=UUID(uid),
        dtstart=datetime(2024, 12, 23, 1, 0, 0, tzinfo=timezone.utc),
        uptime=timedelta(hours=1),
    )


@pytest.fixture
def repository(settings):
    return get_repository(settings)


@pytest.fixture(autouse=True)
def initialize_data(repository, beacon):
    repository.upsert_beacon(beacon)
    repository.upsert_beacon(
        Beacon(
            uid=beacon.uid,
            dtstart=datetime(2025, 1, 7, 20, 30, 40, tzinfo=timezone.utc),
            uptime=timedelta(hours=2),
        )
    )


@pytest.fixture
def client():
    return TestClient(api)


def test_get_beacons(client, beacon):
    response = client.get(f"/beacons/{beacon.uid}")

    assert response.status_code == status.HTTP_200_OK
    assert beacon.model_dump(mode="json") in response.json()


def test_patch_beacons(repository, client, beacon):
    beacon.uptime = timedelta(hours=2)

    response = client.patch(
        f"/beacons/{beacon.uid}", json=beacon.model_dump(mode="json")
    )

    assert response.status_code == status.HTTP_200_OK
    assert beacon in repository.find_beacons(beacon.uid)


def test_patch_beacons_with_unmatching_uid(client, beacon):
    response = client.patch(
        "/beacons/3b9da835-9aa1-4a76-b02d-d2f5b6dd9766",
        json=beacon.model_dump(mode="json"),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_summarize(client, uid):
    response = client.get(f"/summarize/{uid}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"uid": uid, "uptime": 10800}


def test_get_summerize_since(client, uid):
    response = client.get(
        f"/summarize/{uid}",
        params={"since": datetime(2025, 1, 7, 0, 0, 0, tzinfo=timezone.utc)},
    )

    assert response.json() == {"uid": uid, "uptime": 7200}


def test_get_summerize_since_after_dtstart(client, uid):
    response = client.get(
        f"/summarize/{uid}",
        params={"since": datetime(2024, 12, 23, 1, 30, 0, tzinfo=timezone.utc)},
    )

    assert response.json() == {"uid": uid, "uptime": 9000}


def test_get_summerize_unknown_uid(client):
    response = client.get("/summarize/06b1acb3-3f47-4962-91a2-9825b5133378")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "uid": "06b1acb3-3f47-4962-91a2-9825b5133378",
        "uptime": 0,
    }


def test_delete_cleanup_unauthenticated(client):
    response = client.delete(
        "/cleanup/", params={"since": datetime(1970, 1, 1, tzinfo=timezone.utc)}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_cleanup(repository, uid, client):
    since = datetime(2025, 1, 1, tzinfo=timezone.utc)
    response = client.delete(
        "/cleanup/",
        params={"since": since},
        auth=("username", "secret"),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"dtstart": "2024-12-23T01:00:00Z", "uid": str(uid), "uptime": 3600}
    ]
    for bcn in client.get(f"/beacons/{uid}").json():
        assert datetime.fromisoformat(bcn["dtstart"]) > since
