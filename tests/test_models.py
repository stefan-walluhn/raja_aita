import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from raja_aita.models import Beacon


class TestBeacon:
    @pytest.fixture
    def uid(self):
        return uuid4()

    @pytest.fixture
    def dtstart(self):
        return datetime(2024, 12, 23, 11, 22, 33, tzinfo=ZoneInfo("Europe/Berlin"))

    @pytest.fixture
    def uptime(self):
        return timedelta(hours=1)

    def test_beacon(self, uid, dtstart, uptime):
        beacon = Beacon(uid=uid, dtstart=dtstart, uptime=uptime)

        assert beacon.uid == uid
        assert beacon.dtstart == dtstart
        assert beacon.uptime == uptime
