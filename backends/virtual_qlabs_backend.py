"""Virtual QBot backend using QLabs/QVL."""

from __future__ import annotations

from backends.base_backend import BaseQBotBackend
from qbot.kinematics import body_to_wheel_speeds
from qbot.state import QBotState


class VirtualQLabsBackend(BaseQBotBackend):
    """Backend for the virtual QBot Platform in QLabs."""

    def __init__(self, actor_number: int = 0, host: str = "localhost") -> None:
        self.actor_number = actor_number
        self.host = host
        self.qlabs = None
        self.qbot_actor = None
        self.connected = False
        self.last_state = QBotState(source="virtual_qlabs", is_stale=True)

    def _load_classes(self):
        try:
            from qvl.qlabs import QuanserInteractiveLabs
            from qvl.qbot_platform import QLabsQBotPlatform
        except ImportError as exc:
            raise RuntimeError(
                "Missing QLabs/QVL Python libraries. Add Quanser_Academic_Resources/0_libraries/python to PYTHONPATH."
            ) from exc
        return QuanserInteractiveLabs, QLabsQBotPlatform

    def connect(self) -> None:
        QuanserInteractiveLabs, QLabsQBotPlatform = self._load_classes()
        self.qlabs = QuanserInteractiveLabs()
        if not self.qlabs.open(self.host):
            raise RuntimeError(f"Could not open QLabs connection to {self.host}")
        self.qbot_actor = QLabsQBotPlatform(self.qlabs)
        self.qbot_actor.spawn_id_degrees(
            actorNumber=self.actor_number,
            location=[0.0, 0.0, 0.1],
            rotation=[0.0, 0.0, 0.0],
            scale=[1.0, 1.0, 1.0],
            configuration=1,
            waitForConfirmation=True,
        )
        self.connected = True
        self.stop()

    def _require_connected(self) -> None:
        if not self.connected or self.qbot_actor is None:
            raise RuntimeError("VirtualQLabsBackend is not connected")

    def _save_state(self, response, left_mps: float, right_mps: float) -> None:
        status = bool(response[0])
        location = response[1]
        gyro_z = float(response[7])
        heading = float(response[8])
        left_encoder = float(response[9])
        right_encoder = float(response[10])
        self.last_state = QBotState(
            x_m=float(location[0]),
            y_m=float(location[1]),
            z_m=float(location[2]),
            yaw_rad=heading,
            left_encoder=left_encoder,
            right_encoder=right_encoder,
            left_wheel_speed=left_mps,
            right_wheel_speed=right_mps,
            gyro_radps=gyro_z,
            source="virtual_qlabs",
            is_stale=not status,
        )

    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        left_mps, right_mps = body_to_wheel_speeds(forward_mps, turn_radps)
        self.set_wheel_speeds(left_mps, right_mps)

    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        self._require_connected()
        response = self.qbot_actor.command_and_request_state(
            right_mps,
            left_mps,
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
        )
        self._save_state(response, left_mps, right_mps)

    def read_state(self) -> QBotState:
        self._require_connected()
        return self.last_state

    def stop(self) -> None:
        if self.connected and self.qbot_actor is not None:
            self.set_wheel_speeds(0.0, 0.0)

    def close(self) -> None:
        if self.connected:
            self.stop()
        if self.qlabs is not None and hasattr(self.qlabs, "close"):
            self.qlabs.close()
        self.connected = False
