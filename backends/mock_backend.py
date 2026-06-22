"""Pure Python mock backend for development without QLabs or hardware."""

from __future__ import annotations

import math
import time

from backends.base_backend import BaseQBotBackend
from qbot.kinematics import body_to_wheel_speeds, wheel_to_body_speeds
from qbot.state import QBotState


class MockBackend(BaseQBotBackend):
    """Mock backend for API and math checks."""

    def __init__(self) -> None:
        self.connected = False
        self.state = QBotState(source="mock")
        self.last_update_s = time.perf_counter()

    def _require_connected(self) -> None:
        if not self.connected:
            raise RuntimeError("MockBackend is not connected. Call connect() first.")

    def _integrate_state(self) -> None:
        """Integrate x, y, and yaw using current velocity."""

        now_s = time.perf_counter()
        dt_s = now_s - self.last_update_s
        self.last_update_s = now_s

        if dt_s <= 0.0:
            return

        yaw_mid = self.state.yaw_rad + 0.5 * self.state.turn_radps * dt_s
        self.state.x_m += self.state.forward_mps * math.cos(yaw_mid) * dt_s
        self.state.y_m += self.state.forward_mps * math.sin(yaw_mid) * dt_s
        self.state.yaw_rad += self.state.turn_radps * dt_s
        self.state.gyro_radps = self.state.turn_radps
        self.state.timestamp_s = now_s

    def connect(self) -> None:
        """Mark mock backend as connected."""

        self.connected = True
        self.last_update_s = time.perf_counter()
        self.state.timestamp_s = self.last_update_s

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Store body velocity command."""

        self._require_connected()
        self._integrate_state()

        self.state.forward_mps = forward_mps
        self.state.turn_radps = turn_radps
        left_mps, right_mps = body_to_wheel_speeds(forward_mps, turn_radps)
        self.state.left_wheel_speed = left_mps
        self.state.right_wheel_speed = right_mps

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Store wheel speed command."""

        self._require_connected()
        self._integrate_state()

        forward_mps, turn_radps = wheel_to_body_speeds(left_mps, right_mps)
        self.state.forward_mps = forward_mps
        self.state.turn_radps = turn_radps
        self.state.left_wheel_speed = left_mps
        self.state.right_wheel_speed = right_mps

    def read_state(self) -> QBotState:
        """Return current mock state after integrating motion."""

        self._require_connected()
        self._integrate_state()
        return self.state

    def stop(self) -> None:
        """Stop mock movement."""

        if not self.connected:
            return

        self._integrate_state()
        self.state.forward_mps = 0.0
        self.state.turn_radps = 0.0
        self.state.left_wheel_speed = 0.0
        self.state.right_wheel_speed = 0.0
        self.state.gyro_radps = 0.0

    def close(self) -> None:
        """Close mock backend."""

        self.stop()
        self.connected = False
