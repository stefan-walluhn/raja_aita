from abc import ABCMeta, abstractmethod
from tinydb import where

from raja_aita.models import Beacon


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def upsert_beacon(self, beacon): ...

    @abstractmethod
    def find_beacons(self, uid): ...


class TinyDBRepository(Repository):
    def __init__(self, db):
        self.db = db

    def upsert_beacon(self, beacon):
        serialized_beacon = beacon.model_dump(mode="json")

        self.db.upsert(
            serialized_beacon,
            (where("uid") == serialized_beacon["uid"])
            & (where("dtstart") == serialized_beacon["dtstart"]),
        )

    def find_beacons(self, uid):
        return [Beacon(**data) for data in self.db.search(where("uid") == str(uid))]
