"""Quanser CSI camera wrapper.

This is allowed for now because we want to test whether Quanser's CSI wrapper is
good enough before replacing it.
"""

from __future__ import annotations

from qbot.state import CameraFrame


class QuanserCSICamera:
    """Wrapper around Quanser PAL QBotPlatformCSICamera.

    TODO:
    - Import QBotPlatformCSICamera lazily inside start().
    - Convert Quanser image output to CameraFrame.
    - Add frame-rate and dropped-frame counters.
    - Add safe close behavior.
    - Compare with OpenCV direct camera access later.
    """

    def __init__(self, width: int = 640, height: int = 400, fps: float = 60.0) -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self.camera = None
        self.running = False

    def start(self) -> None:
        """Start the CSI camera.

        TODO:
        - Import Quanser class here.
        - Create camera object.
        """

        raise NotImplementedError

    def read(self) -> CameraFrame:
        """Read one CSI frame.

        TODO:
        - Return CameraFrame.
        - Mark dropped or stale frames cleanly.
        """

        raise NotImplementedError

    def stop(self) -> None:
        """Stop the CSI camera.

        TODO:
        - Call terminate on Quanser object if it exists.
        - Make repeated stop calls safe.
        """

        self.running = False
