import datetime
from pydantic import BaseModel, AwareDatetime, UUID4, PlainSerializer
from typing_extensions import Annotated


class Beacon(BaseModel):
    uid: UUID4
    dtstart: AwareDatetime
    uptime: Annotated[
        datetime.timedelta,
        PlainSerializer(lambda x: x.seconds, return_type=int, when_used="json"),
    ]
