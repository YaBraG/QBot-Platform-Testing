"""QBot command limit helpers."""

from __future__ import annotations

from qbot.constants import MAX_EDUCATION_LINEAR_SPEED_MPS, MAX_EDUCATION_TURN_SPEED_RADPS


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def clamp_body_velocity(forward_mps: float, turn_radps: float) -> tuple[float, float]:
    forward = clamp(forward_mps, -MAX_EDUCATION_LINEAR_SPEED_MPS, MAX_EDUCATION_LINEAR_SPEED_MPS)
    turn = clamp(turn_radps, -MAX_EDUCATION_TURN_SPEED_RADPS, MAX_EDUCATION_TURN_SPEED_RADPS)
    return forward, turn


def clamp_wheel_speeds(left_mps: float, right_mps: float) -> tuple[float, float]:
    left = clamp(left_mps, -MAX_EDUCATION_LINEAR_SPEED_MPS, MAX_EDUCATION_LINEAR_SPEED_MPS)
    right = clamp(right_mps, -MAX_EDUCATION_LINEAR_SPEED_MPS, MAX_EDUCATION_LINEAR_SPEED_MPS)
    return left, right
