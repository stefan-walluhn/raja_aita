from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from .config import get_settings
from .repositories import Repository, TinyDBRepository


class RepositoryFactory:
    _repository = None

    def __init__(self):
        self.settings = get_settings()

    def __call__(self) -> Repository:
        # XXX not thread safe
        if RepositoryFactory._repository is None:
            if self.settings.tinydb_path is not None:
                db = TinyDB(self.settings.tinydb_path)
            else:
                db = TinyDB(storage=MemoryStorage)
            RepositoryFactory._repository = TinyDBRepository(db)

        return RepositoryFactory._repository
