import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import AwareDatetime
from typing import Annotated, List

from ..config import Settings, get_settings
from ..factories import RepositoryFactory
from ..models import Beacon
from ..repositories import Repository


router = APIRouter()


security = HTTPBasic()


def validate_basic_auth(
    settings: Annotated[Settings, Depends(get_settings)],
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> bool:
    username = credentials.username.encode("utf8")
    password = credentials.password.encode("utf8")

    valid_username = settings.cleanup_username.encode("utf8")
    valid_password = settings.cleanup_password.encode("utf8")

    return secrets.compare_digest(username, valid_username) and secrets.compare_digest(
        password, valid_password
    )


@router.delete("/")
async def delete_cleanup(
    valid_basic_auth: Annotated[bool, Depends(validate_basic_auth)],
    repository: Annotated[Repository, Depends(RepositoryFactory())],
    since: AwareDatetime,
) -> List[Beacon]:
    if not valid_basic_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

    beacons = filter(lambda b: b.dtstart + b.uptime < since, repository.all())
    repository.delete_beacons(beacons)

    return beacons
