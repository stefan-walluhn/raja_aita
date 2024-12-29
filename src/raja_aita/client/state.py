from datetime import datetime
from pydantic import BaseModel, AwareDatetime


class State(BaseModel):
    is_awake: bool = True
    awake_since: AwareDatetime = datetime.now().astimezone()


class StateManager:
    def __init__(self, state: State) -> None:
        self.state = state

    def sleep(self) -> None:
        self.state.is_awake = False

    def wake_up(self, awake_since: AwareDatetime | None = None) -> None:
        if awake_since is not None:
            self.state.awake_since = awake_since
        else:
            self.state.awake_since = datetime.now().astimezone()
        self.state.is_awake = True
