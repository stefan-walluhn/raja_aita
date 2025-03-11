from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from typing import Annotated, Iterable

from ..factories import RepositoryFactory
from ..models import Beacon
from ..repositories import Repository


router = APIRouter()


@router.get("/{uid}")
async def get_beacons(
    uid: UUID4, repository: Annotated[Repository, Depends(RepositoryFactory())]
) -> Iterable[Beacon]:
    return repository.find_beacons(uid)


@router.patch("/{uid}")
async def patch_beacon(
    uid: UUID4,
    beacon: Beacon,
    repository: Annotated[Repository, Depends(RepositoryFactory())],
) -> Beacon:
    # XXX dedicated beacon_in?
    if uid != beacon.uid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="uid of route does not match beacon",
        )

    repository.upsert_beacon(beacon)
    return beacon
