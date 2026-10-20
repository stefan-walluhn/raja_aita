from datetime import UTC, datetime
from typing import Any

import dbus
from pydantic import UUID4

from ..models import Beacon
from .gateway import Gateway
from .state import State, StateManager


class DBusSignalReceiver:
    def __init__(self, state_manager: StateManager) -> None:
        self.state_manager = state_manager

    def __call__(self, _: dbus.String, data: dbus.Dictionary, *args: list[Any]) -> None:
        # XXX _ == 'org.freedesktop.login1.???'
        if "IdleHint" in data:
            if data["IdleHint"]:
                self.state_manager.sleep()
            else:
                if data["IdleSinceHint"] == 0:
                    return

                self.state_manager.wake_up(
                    datetime.fromtimestamp(
                        data["IdleSinceHint"] / 1000000, UTC
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
                uptime=datetime.now(tz=UTC) - self.state.awake_since,
            )
            self.gateway.patch_beacon(beacon)

        return True
