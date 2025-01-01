import pytest
from datetime import datetime, timezone
from unittest.mock import Mock

from raja_aita.client.gateway import Gateway
from raja_aita.client.receiver import DBusSignalReceiver, TimerReceiver
from raja_aita.client.state import State, StateManager


class TestDBusSignalReceiver:
    @pytest.fixture
    def state_manager(self):
        return Mock(spec=StateManager)

    @pytest.fixture
    def receiver(self, state_manager):
        return DBusSignalReceiver(state_manager)

    def test_call_with_idle_hint_true(self, state_manager, receiver):
        receiver(None, {"IdleHint": True})

        state_manager.sleep.assert_called_once()
        state_manager.wake_up.assert_not_called()

    def test_call_with_idle_hint_false(self, state_manager, receiver):
        receiver(None, {"IdleHint": False, "IdleSinceHint": 1735741149885606})

        state_manager.wake_up.assert_called_once_with(
            datetime(2025, 1, 1, 14, 19, 9, tzinfo=timezone.utc)
        )
        state_manager.sleep.assert_not_called()

    def test_call_with_unknown_message(self, state_manager, receiver):
        receiver(None, {"Foo": "Bar"})

        state_manager.sleep.assert_not_called()
        state_manager.wake_up.assert_not_called()


class TestTimerReciver:
    def test_call_when_is_awake(self):
        state = State(is_awake=True, awake_since=datetime.now().astimezone())
        gateway = Mock(spec=Gateway)

        receiver = TimerReceiver(state, gateway)

        receiver()

        gateway.patch_beacon.assert_called_once()

    def test_call_when_is_not_awake(self):
        state = State(is_awake=False, awake_since=datetime.now().astimezone())
        gateway = Mock(spec=Gateway)

        receiver = TimerReceiver(state, gateway)

        receiver()

        gateway.patch_beacon.assert_not_called()
