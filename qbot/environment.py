"""Environment detection for virtual, physical, or mock QBot execution.

This module must stay independent from Quanser imports.
"""

from __future__ import annotations

import os
import platform


QBOT_MODE_ENV_VAR = "QBOT_MODE"
MODE_PHYSICAL = "physical"
MODE_VIRTUAL = "virtual"
MODE_MOCK = "mock"


def get_username() -> str:
    """Return the current username without crashing in services."""

    try:
        return os.getlogin()
    except OSError:
        return os.getenv("USER", "") or os.getenv("USERNAME", "")


def get_mode_override() -> str | None:
    """Read QBOT_MODE.

    TODO:
    - Validate allowed values in one place.
    - Add tests for empty, physical, virtual, mock, and invalid values.
    """

    value = os.getenv(QBOT_MODE_ENV_VAR, "").strip().lower()
    return value or None


def is_physical_qbot() -> bool:
    """Return True if this machine looks like the physical QBot Platform.

    TODO:
    - Keep QBOT_MODE override support.
    - Improve auto detection beyond username and CPU architecture.
    - Avoid any imports that only work on the QBot.
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
    """Return the selected runtime mode.

    TODO:
    - Use this inside QBotMover.
    - Decide whether invalid QBOT_MODE values should raise an exception.
    """

    override = get_mode_override()

    if override in {MODE_PHYSICAL, MODE_VIRTUAL, MODE_MOCK}:
        return override

    if is_physical_qbot():
        return MODE_PHYSICAL

    return MODE_VIRTUAL
