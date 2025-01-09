from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from functools import reduce
from pydantic import AwareDatetime, UUID4
from typing import Annotated

from ..factories import RepositoryFactory
from ..models import Summary
from ..repositories import Repository

_DEFAULT_SINCE = datetime.fromtimestamp(0, tz=timezone.utc)

router = APIRouter()


@router.get("/{uid}")
async def get_summarize(
    uid: UUID4, repository: Annotated[Repository, Depends(RepositoryFactory())],
    since: AwareDatetime = _DEFAULT_SINCE,
) -> Summary:
    uptime = reduce(
        lambda x, y: x + y,
        map(
            lambda b: b.uptime if b.dtstart > since else since - b.dtstart,
            filter(
                lambda b: b.dtstart + b.uptime >= since,
                repository.find_beacons(uid)
            )
        ),
        timedelta(0)
    )

    return Summary(uid=uid, uptime=uptime)
