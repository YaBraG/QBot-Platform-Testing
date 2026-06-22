"""Direct Intel RealSense wrapper using pyrealsense2.

This wrapper should avoid Quanser multimedia and use RealSense SDK features such
as depth-to-color alignment.
"""

from __future__ import annotations

import numpy as np

class RealSenseFrameSet:
    """Color and depth frames from RealSense.

    TODO:
    - Add intrinsics.
    - Add frame timestamps.
    - Add aligned-depth flag.
    """

    color_bgr: np.ndarray | None = None
    depth_raw: np.ndarray | None = None
    depth_meters: np.ndarray | None = None
    aligned_to_color: bool = False


class RealSenseDirectCamera:
    """Direct RealSense SDK camera wrapper.

    TODO:
    - Import pyrealsense2 lazily inside start().
    - Start color and depth streams.
    - Use depth-to-color alignment.
    - Return RealSenseFrameSet from read().
    - Add resolution and FPS fallback options.
    - Compare output against Quanser RealSense if needed.
    """

    def __init__(self, width: int = 640, height: int = 480, fps: int = 30) -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self.pipeline = None
        self.align = None
        self.depth_scale = None
        self.running = False

    def start(self) -> None:
        """Start RealSense streams.

        TODO:
        - Import pyrealsense2 here.
        - Configure color and depth streams.
        - Create alignment object.
        """

        raise NotImplementedError

    def read(self) -> RealSenseFrameSet:
        """Read aligned color and depth frames.

        TODO:
        - Wait for frames.
        - Align depth to color.
        - Convert depth to meters.
        """

        raise NotImplementedError

    def stop(self) -> None:
        """Stop RealSense streams.

        TODO:
        - Stop pipeline if running.
        - Make repeated stop calls safe.
        """

        self.running = False
