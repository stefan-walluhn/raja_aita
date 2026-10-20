from datetime import UTC, datetime, timedelta
from functools import reduce
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import UUID4, AwareDatetime

from ..models import Summary
from ..repositories import Repository
from . import get_repository

_DEFAULT_SINCE = datetime.fromtimestamp(0, tz=UTC)

router = APIRouter()


@router.get("/{uid}")
async def get_summarize(
    uid: UUID4,
    repository: Annotated[Repository, Depends(get_repository)],
    since: AwareDatetime = _DEFAULT_SINCE,
) -> Summary:
    uptime = reduce(
        lambda x, y: x + y,
        map(
            lambda b: b.uptime if b.dtstart > since else since - b.dtstart,
            filter(
                lambda b: b.dtstart + b.uptime >= since, repository.find_beacons(uid)
            ),
        ),
        timedelta(0),
    )

    return Summary(uid=uid, uptime=uptime)
