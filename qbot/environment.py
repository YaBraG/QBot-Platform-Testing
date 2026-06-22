"""Runtime environment selection for the QBot project.

This module must stay independent from Quanser imports so it can run on any
normal development machine.
"""

from __future__ import annotations

import os
import platform


QBOT_MODE_ENV_VAR = "QBOT_MODE"
MODE_PHYSICAL = "physical"
MODE_VIRTUAL = "virtual"
MODE_MOCK = "mock"


def get_username() -> str:
    """Return the current username without crashing in services.

    TODO:
    - Add tests for Windows, Linux, and service-style environments.
    """

    try:
        return os.getlogin()
    except OSError:
        return os.getenv("USER", "") or os.getenv("USERNAME", "")


def get_mode_override() -> str | None:
    """Read QBOT_MODE.

    TODO:
    - Validate allowed values in one place.
    - Decide whether invalid values should raise an error or print a warning.
    """

    value = os.getenv(QBOT_MODE_ENV_VAR, "").strip().lower()
    return value or None


def is_physical_qbot() -> bool:
    """Return True if this machine looks like the physical QBot Platform.

    TODO:
    - Keep QBOT_MODE override support.
    - Improve auto detection beyond username and CPU architecture.
    - Add optional physical checks such as known devices or ports.
    """

    override = get_mode_override()

    if override == MODE_PHYSICAL:
        return True

    if override in {MODE_VIRTUAL, MODE_MOCK}:
        return False

    username = get_username()
    machine = platform.machine().lower()

    return username == "nvidia" and machine == "aarch64"


def selected_runtime_mode() -> str:
    """Return physical, virtual, or mock.

    TODO:
    - Use this as the single source of truth inside QBotMover.
    - Add unit tests for override behavior.
    """

    override = get_mode_override()

    if override in {MODE_PHYSICAL, MODE_VIRTUAL, MODE_MOCK}:
        return override

    return MODE_PHYSICAL if is_physical_qbot() else MODE_VIRTUAL
