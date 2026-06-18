"""Virtual QBot backend using QLabs/QVL."""

from __future__ import annotations

from backends.base_backend import BaseQBotBackend
from qbot.kinematics import body_to_wheel_speeds
from qbot.state import QBotState


class VirtualQLabsBackend(BaseQBotBackend):
    """Backend for the virtual QBot Platform in QLabs.

    TODO:
    - Import QLabs and QVL lazily inside connect().
    - Connect to QLabs.
    - Spawn or attach to the QBot actor.
    - Convert our left/right wheel order to the QVL command order.
    - Convert returned virtual state into QBotState.
    """

    def __init__(self, actor_number: int = 0) -> None:
        self.actor_number = actor_number
        self.qlabs = None
        self.qbot_actor = None
        self.connected = False
        self.last_state = QBotState(source="virtual_qlabs")

    def connect(self) -> None:
        """Connect to QLabs and prepare the virtual QBot.

        TODO:
        - Add friendly error if QLabs libraries are missing.
        - Decide whether setup is automatic or manual.
        """

        raise NotImplementedError

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Command virtual QBot by body velocity.

        TODO:
        - Confirm turn sign convention in QLabs.
        """

        left_mps, right_mps = body_to_wheel_speeds(forward_mps, turn_radps)
        self.set_wheel_speeds(left_mps, right_mps)

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Command virtual QBot by wheel speeds.

        TODO:
        - Public API is left, right.
        - QVL command order needs to be handled inside this method.
        - Update last_state after command.
        """

        raise NotImplementedError

    def read_state(self) -> QBotState:
        """Return latest virtual state.

        TODO:
        - Decide whether this requests fresh state or returns cached state.
        """

        return self.last_state

    def stop(self) -> None:
        """Stop virtual QBot movement.

        TODO:
        - Send zero wheel speeds safely.
        """

        self.set_wheel_speeds(0.0, 0.0)

    def close(self) -> None:
        """Close virtual backend resources.

        TODO:
        - Stop first.
        - Decide whether to close QLabs or leave it open.
        """

        self.connected = False
