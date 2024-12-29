import requests

from raja_aita.models import Beacon


class Gateway:
    def __init__(self, url: str) -> None:
        self.url = url

    def patch_beacon(self, beacon: Beacon) -> None:
        requests.patch(
            "/".join([self.url, "beacons", str(beacon.uid)]),
            json=beacon.model_dump(mode="json"),
        )
