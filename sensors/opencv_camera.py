"""OpenCV camera fallback wrapper.

Use this if Quanser CSI is not good enough or if we need a simple generic USB or
Linux camera path.
"""

from __future__ import annotations

from qbot.state import CameraFrame


class OpenCVCamera:
    """Generic OpenCV camera wrapper.

    TODO:
    - Implement cv2.VideoCapture start/read/stop.
    - Add camera index or device path support.
    - Add width, height, FPS settings.
    - Compare against Quanser CSI on physical QBot.
    """

    def __init__(self, camera_id: int | str = 0, width: int = 640, height: int = 480, fps: float = 30.0) -> None:
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        self.capture = None
        self.running = False

    def start(self) -> None:
        """Start OpenCV camera.

        TODO:
        - Import cv2 lazily here.
        - Open VideoCapture.
        - Set frame properties.
        """

        raise NotImplementedError

    def read(self) -> CameraFrame:
        """Read one frame.

        TODO:
        - Return CameraFrame.
        - Handle failed reads.
        """

        raise NotImplementedError

    def stop(self) -> None:
        """Stop OpenCV camera.

        TODO:
        - Release capture object.
        - Make repeated stop calls safe.
        """

        self.running = False
