from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from uuid import UUID

from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

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

    def all(self) -> list[Beacon]:
        return [Beacon(**data) for data in self.db.all()]

    def upsert_beacon(self, beacon: Beacon) -> None:
        dumped_beacon = beacon.model_dump(mode="json")

        self.db.upsert(
            dumped_beacon,
            (where("uid") == dumped_beacon["uid"])
            & (where("dtstart") == dumped_beacon["dtstart"]),
        )

    def find_beacons(self, uid: UUID) -> list[Beacon]:
        return [Beacon(**data) for data in self.db.search(where("uid") == str(uid))]

    def delete_beacons(self, beacons: Iterable[Beacon]) -> None:
        for b in [beacon.model_dump(mode="json") for beacon in beacons]:
            self.db.remove(
                (where("uid") == b["uid"]) & (where("dtstart") == b["dtstart"])
            )


class Factory:
    _repository: Repository | None = None

    def __init__(self, tinydb_path: Path | None = None):
        self.tinydb_path = tinydb_path

    def __call__(self) -> Repository:
        # XXX not thread safe
        if Factory._repository is None:
            if self.tinydb_path is not None:
                db = TinyDB(self.tinydb_path)
            else:
                db = TinyDB(storage=MemoryStorage)
            Factory._repository = TinyDBRepository(db)

        return Factory._repository
