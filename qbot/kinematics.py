"""Differential-drive math for the QBot Platform."""

from __future__ import annotations

from qbot.constants import WHEEL_BASE_M


def body_to_wheel_speeds(forward_mps: float, turn_radps: float, wheel_base_m: float = WHEEL_BASE_M) -> tuple[float, float]:
    """Convert body velocity to left and right wheel linear speeds.

    TODO:
    - Confirm sign convention in QLabs.
    - Confirm sign convention on the physical QBot.
    - Add tests for straight, left turn, right turn, and spin-in-place.
    """

    left_mps = forward_mps - (turn_radps * wheel_base_m / 2.0)
    right_mps = forward_mps + (turn_radps * wheel_base_m / 2.0)
    return left_mps, right_mps


def wheel_to_body_speeds(left_mps: float, right_mps: float, wheel_base_m: float = WHEEL_BASE_M) -> tuple[float, float]:
    """Convert left and right wheel speeds to body velocity.

    TODO:
    - Use this in MockBackend state integration.
    - Add tests against body_to_wheel_speeds.
    """

    forward_mps = (left_mps + right_mps) / 2.0
    turn_radps = (right_mps - left_mps) / wheel_base_m
    return forward_mps, turn_radps
