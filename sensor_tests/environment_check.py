"""Print basic environment information for QBot Platform tests.

This script does not import Quanser libraries. It is only used to see whether
our own code should treat the machine as a physical QBot or as a virtual/dev PC.
"""

from __future__ import annotations

import os
import platform


def is_physical_qbot() -> bool:
    """Return True when the current machine looks like the physical QBot.

    Manual override:
        QBOT_MODE=physical
        QBOT_MODE=virtual
    """

    mode_override = os.getenv("QBOT_MODE", "").strip().lower()

    if mode_override == "physical":
        return True

    if mode_override == "virtual":
        return False

    try:
        username = os.getlogin()
    except OSError:
        username = os.getenv("USER", "") or os.getenv("USERNAME", "")

    machine = platform.machine().lower()

    return username == "nvidia" and machine == "aarch64"


def main() -> None:
    try:
        username = os.getlogin()
    except OSError:
        username = os.getenv("USER", "") or os.getenv("USERNAME", "")

    print("QBot environment check")
    print("----------------------")
    print(f"OS:              {platform.system()} {platform.release()}")
    print(f"Architecture:    {platform.machine()}")
    print(f"Username:        {username}")
    print(f"QBOT_MODE env:   {os.getenv('QBOT_MODE', '<not set>')}")
    print(f"IS_PHYSICAL:     {is_physical_qbot()}")


if __name__ == "__main__":
    main()
