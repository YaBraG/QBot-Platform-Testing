"""Shared QBot Platform constants.

Values here should use SI units unless the name clearly says otherwise.
"""

from __future__ import annotations


# TODO: Confirm these values against the physical QBot Platform manual.
WHEEL_RADIUS_M = 3.5 * 0.0254 / 2.0
WHEEL_BASE_M = 0.3928
WHEEL_WIDTH_M = 0.04445
ENCODER_COUNTS = 85.0
ENCODER_MODE = 4
COUNTS_PER_REV = ENCODER_COUNTS * ENCODER_MODE

# TODO: Use these for safe defaults in physical tests.
DEFAULT_LINEAR_SPEED_MPS = 0.15
DEFAULT_TURN_SPEED_RADPS = 0.4
MAX_EDUCATION_LINEAR_SPEED_MPS = 0.3
MAX_EDUCATION_TURN_SPEED_RADPS = 1.0

# TODO: Confirm actual sensor frame names we want to use in our code.
FRAME_BASE = "base_link"
FRAME_LIDAR = "lidar"
FRAME_REALSENSE = "realsense"
FRAME_CSI = "downward_camera"
