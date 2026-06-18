"""Quanser LIDAR wrapper.

This is allowed for now because we want to test whether Quanser's LIDAR wrapper
is good enough before replacing it.
"""

from __future__ import annotations

from qbot.state import LidarScan


class QuanserLidar:
    """Wrapper around Quanser PAL QBotPlatformLidar.

    TODO:
    - Import QBotPlatformLidar lazily inside start().
    - Convert Quanser angles and distances to LidarScan.
    - Add scan-rate and valid-point counters.
    - Add filtering helpers later.
    - Compare with direct serial or TCP access later.
    """

    def __init__(self, measurements: int = 1680) -> None:
        self.measurements = measurements
        self.lidar = None
        self.running = False

    def start(self) -> None:
        """Start LIDAR.

        TODO:
        - Import Quanser LIDAR class here.
        - Create LIDAR object.
        """

        raise NotImplementedError

    def read(self) -> LidarScan:
        """Read one LIDAR scan.

        TODO:
        - Return LidarScan.
        - Handle no-scan cases cleanly.
        """

        raise NotImplementedError

    def stop(self) -> None:
        """Stop LIDAR.

        TODO:
        - Call terminate on Quanser object if it exists.
        - Make repeated stop calls safe.
        """

        self.running = False
