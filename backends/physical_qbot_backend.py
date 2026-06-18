"""Physical QBot backend.

This backend is for running on the real QBot Platform. Keep hardware-specific
and Quanser driver-stream code isolated here.
"""

from __future__ import annotations

from backends.base_backend import BaseQBotBackend
from qbot.state import QBotState


class PhysicalQBotBackend(BaseQBotBackend):
    """Backend for the physical QBot Platform.

    TODO:
    - Start with Quanser driver stream only if unavoidable.
    - Hide every Quanser detail from QBotMover.
    - Add strict speed limits.
    - Add watchdog timeout behavior.
    - Always stop on exceptions and close.
    - Add battery and stale-data checks.
    """

    def __init__(self, ip: str = "192.168.2.15", driver_port: int = 18888) -> None:
        self.ip = ip
        self.driver_port = driver_port
        self.connected = False
        self.last_state = QBotState(source="physical_qbot")

    def connect(self) -> None:
        """Connect to the physical QBot driver.

        TODO:
        - Import Quanser driver-stream dependency lazily.
        - Add clear error messages for missing driver or bad IP.
        - Confirm driver mode and arm behavior.
        """

        raise NotImplementedError

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Command body velocity on physical QBot.

        TODO:
        - Clamp speed limits before sending.
        - Require safe calling patterns for long movement.
        - Update last_state from driver feedback.
        """

        raise NotImplementedError

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Command wheel speeds on physical QBot.

        TODO:
        - Confirm whether the driver expects body or wheel mode.
        - Add explicit mode selection.
        """

        raise NotImplementedError

    def read_state(self) -> QBotState:
        """Return latest physical state.

        TODO:
        - Pull fresh driver feedback.
        - Mark state stale if feedback timeout occurs.
        """

        return self.last_state

    def stop(self) -> None:
        """Stop physical QBot.

        TODO:
        - Send zero command.
        - Make this safe to call repeatedly.
        """

        raise NotImplementedError

    def close(self) -> None:
        """Close physical backend.

        TODO:
        - Always call stop before closing.
        - Close driver stream cleanly.
        """

        self.connected = False
