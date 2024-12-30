import logging
import requests

from raja_aita.models import Beacon


logger = logging.getLogger(__name__)


class Gateway:
    def __init__(self, url: str) -> None:
        self.url = url

    def patch_beacon(self, beacon: Beacon) -> None:
        try:
            requests.patch(
                "/".join([self.url, "beacons", str(beacon.uid)]),
                json=beacon.model_dump(mode="json"),
                timeout=30.0,
            )
        except requests.exceptions.RequestException as e:
            logger.error("Failed to transmit beacon: %s", e)
