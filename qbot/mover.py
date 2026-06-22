"""Main user-facing QBot movement API."""

from __future__ import annotations

import time

from qbot.environment import MODE_MOCK, MODE_PHYSICAL, MODE_VIRTUAL, selected_runtime_mode
from qbot.limits import clamp_body_velocity, clamp_wheel_speeds
from qbot.state import QBotState


class QBotMover:
    """High-level QBot movement interface.

    User code should use this class instead of importing a backend directly.
    """

    def __init__(self, force_mode: str | None = None) -> None:
        self.mode = force_mode or selected_runtime_mode()

        if self.mode not in {MODE_VIRTUAL, MODE_PHYSICAL, MODE_MOCK}:
            raise ValueError(f"Unsupported QBot mode: {self.mode}")

        self.backend = self._create_backend(self.mode)

    def _create_backend(self, mode: str):
        """Create the selected backend with lazy imports."""

        if mode == MODE_MOCK:
            from backends.mock_backend import MockBackend

            return MockBackend()

        if mode == MODE_VIRTUAL:
            from backends.virtual_qlabs_backend import VirtualQLabsBackend

            return VirtualQLabsBackend()

        if mode == MODE_PHYSICAL:
            from backends.physical_qbot_backend import PhysicalQBotBackend

            return PhysicalQBotBackend()

        raise ValueError(f"Unsupported QBot mode: {mode}")

    def connect(self) -> None:
        """Connect to the selected backend."""

        self.backend.connect()

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Command forward and turning speed after clamping."""

        limited_forward, limited_turn = clamp_body_velocity(forward_mps, turn_radps)
        self.backend.set_body_velocity(limited_forward, limited_turn)

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Command left and right wheel speeds after clamping."""

        limited_left, limited_right = clamp_wheel_speeds(left_mps, right_mps)
        self.backend.set_wheel_speeds(limited_left, limited_right)

    def drive_for_seconds(self, forward_mps: float, turn_radps: float, seconds: float) -> None:
        """Drive for a fixed duration, then stop."""

        if seconds < 0:
            raise ValueError("seconds must be non-negative")

        self.set_body_velocity(forward_mps, turn_radps)
        try:
            time.sleep(seconds)
        finally:
            self.stop()

    def read_state(self) -> QBotState:
        """Return latest QBot state."""

        return self.backend.read_state()

    def stop(self) -> None:
        """Stop QBot movement."""

        self.backend.stop()

    def close(self) -> None:
        """Close backend resources."""

        self.backend.close()
