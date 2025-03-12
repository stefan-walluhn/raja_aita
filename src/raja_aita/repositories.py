from abc import ABCMeta, abstractmethod
from tinydb import TinyDB, where
from typing import Iterable, List
from uuid import UUID

from .models import Beacon


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def all(self) -> Iterable[Beacon]: ...

    @abstractmethod
    def upsert_beacon(self, beacon: Beacon) -> None: ...

    @abstractmethod
    def find_beacons(self, uid: UUID) -> Iterable[Beacon]: ...

    @abstractmethod
    def delete_beacons(self, beacons: Iterable[Beacon]) -> None: ...


class TinyDBRepository(Repository):
    def __init__(self, db: TinyDB):
        self.db = db

    def all(self) -> List[Beacon]:
        return [Beacon(**data) for data in self.db.all()]

    def upsert_beacon(self, beacon: Beacon) -> None:
        dumped_beacon = beacon.model_dump(mode="json")

        self.db.upsert(
            dumped_beacon,
            (where("uid") == dumped_beacon["uid"])
            & (where("dtstart") == dumped_beacon["dtstart"]),
        )

    def find_beacons(self, uid: UUID) -> List[Beacon]:
        return [Beacon(**data) for data in self.db.search(where("uid") == str(uid))]

    def delete_beacons(self, beacons: Iterable[Beacon]) -> None:
        for b in [beacon.model_dump(mode="json") for beacon in beacons]:
            self.db.remove(
                (where("uid") == b["uid"]) & (where("dtstart") == b["dtstart"])
            )
