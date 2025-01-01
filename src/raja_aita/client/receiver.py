import dbus
from datetime import datetime, timezone
from pydantic import UUID4
from typing import Any

from ..models import Beacon
from .state import State, StateManager
from .gateway import Gateway


class DBusSignalReceiver:
    def __init__(self, state_manager: StateManager) -> None:
        self.state_manager = state_manager

    def __call__(self, _: dbus.String, data: dbus.Dictionary, *args: list[Any]) -> None:
        # XXX _ == 'org.freedesktop.login1.???'
        if "IdleHint" in data:
            if data["IdleHint"]:
                self.state_manager.sleep()
            else:
                self.state_manager.wake_up(
                    datetime.fromtimestamp(
                        data["IdleSinceHint"] / 1000000, timezone.utc
                    )
                )

        # XXX return?


class TimerReceiver:
    def __init__(self, uid: UUID4, state: State, gateway: Gateway) -> None:
        self.uid = uid
        self.state = state
        self.gateway = gateway

    def __call__(self) -> bool:
        if self.state.is_awake:
            # XXX tests
            beacon = Beacon(
                uid=self.uid,
                dtstart=self.state.awake_since,
                uptime=datetime.now(tz=timezone.utc) - self.state.awake_since,
            )
            self.gateway.patch_beacon(beacon)

        return True
