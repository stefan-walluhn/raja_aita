from fastapi import Depends
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from typing import Annotated

from .config import Settings, get_settings
from .repositories import Repository, TinyDBRepository


class RepositoryFactory:
    _repository = None

    def __call__(
        self, settings: Annotated[Settings, Depends(get_settings)]
    ) -> Repository:
        # XXX not thread safe
        if RepositoryFactory._repository is None:
            if settings.tinydb_path is not None:
                db = TinyDB(settings.tinydb_path)
            else:
                db = TinyDB(storage=MemoryStorage)
            RepositoryFactory._repository = TinyDBRepository(db)

        return RepositoryFactory._repository
