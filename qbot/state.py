"""Dataclasses for QBot movement and sensor data."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any


@dataclass
class QBotCommand:
    """Command sent to a movement backend."""

    forward_mps: float = 0.0
    turn_radps: float = 0.0
    left_mps: float | None = None
    right_mps: float | None = None
    timestamp_s: float = 0.0
    duration_s: float | None = None


@dataclass
class QBotState:
    """State returned by a backend."""

    x_m: float = 0.0
    y_m: float = 0.0
    z_m: float = 0.0
    yaw_rad: float = 0.0
    forward_mps: float = 0.0
    turn_radps: float = 0.0
    left_encoder: float = 0.0
    right_encoder: float = 0.0
    left_wheel_speed: float = 0.0
    right_wheel_speed: float = 0.0
    gyro_radps: float = 0.0
    battery_voltage: float | None = None
    timestamp_s: float = 0.0
    source: str = "unknown"
    is_stale: bool = False

    @property
    def yaw_deg(self) -> float:
        return math.degrees(self.yaw_rad)


@dataclass
class LidarScan:
    """Simple LIDAR scan container."""

    angles_rad: Any = None
    distances_m: Any = None
    timestamp_s: float = 0.0
    source: str = "unknown"


@dataclass
class CameraFrame:
    """Simple camera frame container."""

    image_bgr: Any = None
    timestamp_s: float = 0.0
    source: str = "unknown"
