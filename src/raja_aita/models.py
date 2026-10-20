import datetime
from typing import Annotated

from pydantic import UUID4, AwareDatetime, BaseModel, PlainSerializer


class Beacon(BaseModel):
    uid: UUID4
    dtstart: AwareDatetime
    uptime: Annotated[
        datetime.timedelta,
        PlainSerializer(lambda x: x.seconds, return_type=int, when_used="json"),
    ]


class Summary(BaseModel):
    uid: UUID4
    uptime: Annotated[
        datetime.timedelta,
        PlainSerializer(lambda x: x.seconds, return_type=int, when_used="json"),
    ]
