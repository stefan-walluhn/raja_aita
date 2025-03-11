from fastapi import APIRouter, Depends
from pydantic import AwareDatetime
from typing import Annotated

from ..factories import RepositoryFactory
from ..repositories import Repository


router = APIRouter()


@router.delete("/")
async def delete_cleanup(
    repository: Annotated[Repository, Depends(RepositoryFactory())],
    since: AwareDatetime,
) -> None:
    repository.delete_beacons(
        filter(lambda b: b.dtstart + b.uptime < since, repository.all())
    )
