import click

from datetime import datetime, timezone
from dbus import SystemBus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from .gateway import Gateway
from .state import State, StateManager
from .receiver import DBusSignalReceiver, TimerReceiver


@click.command()
@click.option("-a", "--api-url", default="http://127.0.0.1:8000", help="API URL")
@click.option("-i", "--interval", type=int, default=60)
@click.argument("uid", type=click.UUID)
def main(api_url, interval, uid):
    gateway = Gateway(api_url)
    state = State(is_awake=True, awake_since=datetime.now(tz=timezone.utc))
    dbus_receiver = DBusSignalReceiver(StateManager(state))
    timer_receiver = TimerReceiver(uid, state, gateway)

    DBusGMainLoop(set_as_default=True)

    bus = SystemBus()
    bus.add_signal_receiver(dbus_receiver, bus_name="org.freedesktop.login1")

    GLib.timeout_add_seconds(interval, timer_receiver)

    loop = GLib.MainLoop()
    loop.run()
