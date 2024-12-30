import pytest

from datetime import datetime, timedelta
from requests.exceptions import RequestException
from uuid import uuid4

from raja_aita.models import Beacon
from raja_aita.client.gateway import Gateway


class TestGateway:
    @pytest.fixture
    def beacon(self):
        return Beacon(
            uid=uuid4(), dtstart=datetime.now().astimezone(), uptime=timedelta(hours=2)
        )

    @pytest.fixture
    def gateway(self):
        return Gateway("https://api.example.test")

    def test_patch_beacon(self, requests_mock, gateway, beacon):
        (uid,) = beacon.model_dump(mode="json", include=["uid"]).values()
        requests_mock.patch("/".join([gateway.url, "beacons", uid]))

        gateway.patch_beacon(beacon)

        assert requests_mock.called
        assert requests_mock.last_request.json() == beacon.model_dump(mode="json")

    def test_patch_beacon_request_error(self, caplog, requests_mock, gateway, beacon):
        (uid,) = beacon.model_dump(mode="json", include=["uid"]).values()
        requests_mock.patch(
            "/".join([gateway.url, "beacons", uid]),
            exc=RequestException("something went wrng"),
        )

        gateway.patch_beacon(beacon)

        assert "Failed to transmit beacon: something went wrng" in caplog.messages
