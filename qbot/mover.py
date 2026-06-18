"""Main user-facing QBot movement API."""

from __future__ import annotations

from qbot.environment import MODE_MOCK, MODE_PHYSICAL, MODE_VIRTUAL, selected_runtime_mode
from qbot.state import QBotState


class QBotMover:
    """High-level QBot movement interface.

    User code should use this class instead of importing a backend directly.

    TODO:
    - Instantiate the correct backend based on selected_runtime_mode().
    - Add force_mode support for virtual, physical, and mock.
    - Add drive_forward, turn_degrees, stop, and close helpers.
    - Keep physical movement safe by requiring timeouts or stop conditions.
    """

    def __init__(self, force_mode: str | None = None) -> None:
        self.mode = force_mode or selected_runtime_mode()
        self.backend = None

        # TODO: Import backend classes lazily here so Quanser imports are isolated.
        # if self.mode == MODE_VIRTUAL:
        #     from backends.virtual_qlabs_backend import VirtualQLabsBackend
        #     self.backend = VirtualQLabsBackend()
        # elif self.mode == MODE_PHYSICAL:
        #     from backends.physical_qbot_backend import PhysicalQBotBackend
        #     self.backend = PhysicalQBotBackend()
        # elif self.mode == MODE_MOCK:
        #     from backends.mock_backend import MockBackend
        #     self.backend = MockBackend()

        if self.mode not in {MODE_VIRTUAL, MODE_PHYSICAL, MODE_MOCK}:
            raise ValueError(f"Unsupported QBot mode: {self.mode}")

    def connect(self) -> None:
        """Connect to the selected backend.

        TODO:
        - Delegate to backend.connect().
        - Raise a helpful error if no backend is loaded yet.
        """

        raise NotImplementedError

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Command forward and turning speed.

        TODO:
        - Validate speed limits.
        - Delegate to backend.set_body_velocity().
        """

        raise NotImplementedError

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Command left and right wheel speeds.

        TODO:
        - Keep public order as left, right.
        - Let the virtual backend convert to Quanser's expected order.
        """

        raise NotImplementedError

    def read_state(self) -> QBotState:
        """Return latest QBot state.

        TODO:
        - Delegate to backend.read_state().
        - Return QBotState with source field filled.
        """

        raise NotImplementedError

    def stop(self) -> None:
        """Stop QBot movement.

        TODO:
        - Always call this in finally blocks in physical examples.
        - Delegate to backend.stop().
        """

        raise NotImplementedError

    def close(self) -> None:
        """Close backend resources.

        TODO:
        - Stop first, then close connections.
        - Make repeated close calls safe.
        """

        raise NotImplementedError
