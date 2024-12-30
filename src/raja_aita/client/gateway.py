import logging
import requests

from raja_aita.models import Beacon


logger = logging.getLogger(__name__)


class Gateway:
    def __init__(self, url: str) -> None:
        self.url = url

    def patch_beacon(self, beacon: Beacon) -> None:
        dumped_beacon = beacon.model_dump(mode="json")

        try:
            requests.patch(
                "/".join([self.url, "beacons", dumped_beacon["uid"]]),
                json=dumped_beacon,
                timeout=30.0,
            )
        except requests.exceptions.RequestException as e:
            logger.error("Failed to transmit beacon: %s", e)
