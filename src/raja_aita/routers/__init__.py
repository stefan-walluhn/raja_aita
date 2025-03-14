from fastapi import Depends
from functools import lru_cache
from typing import Annotated

from ..repositories import Repository, Factory as RepositoryFactory
from ..settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_repository(settings: Annotated[Settings, Depends(get_settings)]) -> Repository:
    return RepositoryFactory(tinydb_path=settings.tinydb_path)()
