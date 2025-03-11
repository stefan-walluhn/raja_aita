import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

from raja_aita.models import Beacon
from raja_aita.repositories import TinyDBRepository


class TestTinyDBRepository:
    @pytest.fixture
    def db(self):
        return TinyDB(storage=MemoryStorage)

    @pytest.fixture
    def repository(self, db):
        return TinyDBRepository(db)

    def test_upsert_beacon_previous_existing(self, db, repository):
        beacon = Beacon(
            uid=uuid4(),
            dtstart=datetime(
                2024, 12, 20, 10, 11, 22, tzinfo=ZoneInfo("Europe/Berlin")
            ),
            uptime=timedelta(hours=2),
        )
        db.insert(
            Beacon(
                uid=beacon.uid, dtstart=beacon.dtstart, uptime=timedelta(hours=1)
            ).model_dump(mode="json")
        )

        repository.upsert_beacon(beacon)

        uid, uptime = beacon.model_dump(mode="json", include=["uid", "uptime"]).values()
        results = db.search(where("uid") == uid)

        assert len(results) == 1
        assert results[0]["uptime"] == uptime

    def test_upsert_beacon_non_existing(self, db, repository):
        beacon = Beacon(
            uid=uuid4(),
            dtstart=datetime(
                2024, 12, 21, 12, 13, 14, tzinfo=ZoneInfo("Europe/Berlin")
            ),
            uptime=timedelta(hours=1),
        )

        repository.upsert_beacon(beacon)

        (uid,) = beacon.model_dump(mode="json", include=["uid"]).values()
        results = db.search(where("uid") == uid)

        assert len(results) == 1
        assert results[0]["uid"] == uid

    def test_find_beacons(self, db, repository):
        uid = uuid4()
        db.insert_multiple(
            [
                b.model_dump(mode="json")
                for b in [
                    Beacon(
                        uid=uid,
                        dtstart=datetime(
                            2024, 12, 20, 8, 9, 10, tzinfo=ZoneInfo("Europe/Berlin")
                        ),
                        uptime=timedelta(hours=1),
                    ),
                    Beacon(
                        uid=uid,
                        dtstart=datetime(
                            2024, 12, 20, 9, 10, 11, tzinfo=ZoneInfo("Asia/Tokyo")
                        ),
                        uptime=timedelta(hours=2),
                    ),
                ]
            ]
        )

        results = repository.find_beacons(uid)

        assert len(results) == 2
        for result in results:
            assert isinstance(result, Beacon)
            assert result.uid == uid

    def test_delete_beacons(self, db, repository):
        beacon = Beacon(
            uid=uuid4(),
            dtstart=datetime(2025, 3, 8, 19, 12, tzinfo=ZoneInfo("Europe/Berlin")),
            uptime=timedelta(hours=1),
        )
        db.insert(beacon.model_dump(mode="json"))

        repository.delete_beacons([beacon])

        assert repository.find_beacons(beacon.uid) == []
