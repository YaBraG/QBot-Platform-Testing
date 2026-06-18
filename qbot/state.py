"""Dataclasses for QBot movement and sensor data."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class QBotCommand:
    """Command sent to a movement backend.

    TODO:
    - Decide whether body velocity, wheel velocity, or both should be stored.
    - Add speed-limit validation.
    - Add optional duration for safer physical commands.
    """

    forward_mps: float = 0.0
    turn_radps: float = 0.0
    left_mps: float | None = None
    right_mps: float | None = None
    timestamp_s: float = 0.0


@dataclass
class QBotState:
    """State returned by a backend.

    TODO:
    - Decide which fields are required for virtual and physical modes.
    - Add helper methods for heading in degrees.
    - Add flags for missing, stale, or low-confidence data.
    """

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


@dataclass
class LidarScan:
    """Simple LIDAR scan container.

    TODO:
    - Add filtering helpers for invalid ranges.
    - Add polar-to-XY conversion.
    """

    angles_rad: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.float64))
    distances_m: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.float64))
    timestamp_s: float = 0.0
    source: str = "unknown"


@dataclass
class CameraFrame:
    """Simple camera frame container.

    TODO:
    - Add camera intrinsics later.
    - Add optional frame ID later.
    """

    image_bgr: np.ndarray | None = None
    timestamp_s: float = 0.0
    source: str = "unknown"
