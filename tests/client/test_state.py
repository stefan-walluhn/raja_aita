from datetime import datetime
from freezegun import freeze_time

from raja_aita.client.state import State, StateManager


class TestStateManager:
    def test_sleep(self):
        state = State(is_awake=True)
        state_manager = StateManager(state)

        state_manager.sleep()

        assert not state.is_awake

    @freeze_time("2024-12-29 10:20:30")
    def test_wake_up(self):
        state = State(
            is_awake=False,
            awake_since=datetime(1999, 12, 29, 10, 20, 30).astimezone(),
        )
        state_manager = StateManager(state)

        state_manager.wake_up()

        assert state.is_awake
        assert state.awake_since == datetime.now().astimezone()

    def test_wake_up_with_time(self):
        awake_since = datetime(2024, 12, 29, 11, 22, 33).astimezone()
        state = State(
            is_awake=False,
            awake_since=datetime(1999, 12, 29, 10, 20, 30).astimezone(),
        )
        state_manager = StateManager(state)

        state_manager.wake_up(awake_since)

        assert state.awake_since == awake_since
