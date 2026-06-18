"""Pure Python mock backend for development without QLabs or hardware."""

from __future__ import annotations

import time

from backends.base_backend import BaseQBotBackend
from qbot.kinematics import body_to_wheel_speeds
from qbot.state import QBotState


class MockBackend(BaseQBotBackend):
    """Mock backend for math and API checks.

    TODO:
    - Integrate differential-drive motion over time.
    - Simulate encoder counts and gyro.
    - Add optional fake noise for filter testing.
    """

    def __init__(self) -> None:
        self.connected = False
        self.state = QBotState(source="mock")
        self.last_update_s = time.perf_counter()

    def connect(self) -> None:
        """Mark mock backend as connected.

        TODO:
        - Reset timer and initial state if needed.
        """

        self.connected = True
        self.last_update_s = time.perf_counter()

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Store body velocity command.

        TODO:
        - Update pose before changing the command.
        - Store command for later integration.
        """

        self.state.forward_mps = forward_mps
        self.state.turn_radps = turn_radps
        left_mps, right_mps = body_to_wheel_speeds(forward_mps, turn_radps)
        self.state.left_wheel_speed = left_mps
        self.state.right_wheel_speed = right_mps

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Store wheel speed command.

        TODO:
        - Convert wheel speeds back to body velocity.
        - Update pose before changing the command.
        """

        self.state.left_wheel_speed = left_mps
        self.state.right_wheel_speed = right_mps

    def read_state(self) -> QBotState:
        """Return current mock state.

        TODO:
        - Integrate x, y, and yaw before returning.
        """

        return self.state

    def stop(self) -> None:
        """Stop mock movement."""

        self.set_body_velocity(0.0, 0.0)

    def close(self) -> None:
        """Close mock backend."""

        self.stop()
        self.connected = False
