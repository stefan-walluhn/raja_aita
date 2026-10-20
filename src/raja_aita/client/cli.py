from datetime import UTC, datetime

import click
from dbus import SystemBus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from pydantic.types import UUID4

from .gateway import Gateway
from .receiver import DBusSignalReceiver, TimerReceiver
from .state import State, StateManager


@click.command()
@click.option("-a", "--api-url", default="http://127.0.0.1:8000", help="API URL")
@click.option("-i", "--interval", type=int, default=60)
@click.argument("uid", type=click.UUID)
def main(api_url: str, interval: int, uid: UUID4) -> None:
    gateway = Gateway(api_url)
    state = State(is_awake=True, awake_since=datetime.now(tz=UTC))
    dbus_receiver = DBusSignalReceiver(StateManager(state))
    timer_receiver = TimerReceiver(uid, state, gateway)

    DBusGMainLoop(set_as_default=True)

    bus = SystemBus()
    bus.add_signal_receiver(dbus_receiver, bus_name="org.freedesktop.login1")

    GLib.timeout_add_seconds(interval, timer_receiver)

    loop = GLib.MainLoop()
    loop.run()
