from uuid import uuid4
from datetime import datetime, timedelta

from raja_aita.models import Beacon
from raja_aita.client.gateway import Gateway


class TestGateway:
    def test_patch_beacon(self, requests_mock):
        beacon = Beacon(
            uid=uuid4(), dtstart=datetime.now().astimezone(), uptime=timedelta(hours=2)
        )
        gateway = Gateway("https://api.example.com")
        requests_mock.patch("/".join([gateway.url, "beacons", str(beacon.uid)]))

        gateway.patch_beacon(beacon)

        assert requests_mock.called
        assert requests_mock.last_request.json() == beacon.model_dump(mode="json")
