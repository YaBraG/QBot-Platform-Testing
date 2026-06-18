"""Base movement backend interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from qbot.state import QBotState


class BaseQBotBackend(ABC):
    """Abstract interface for all QBot movement backends.

    TODO:
    - Decide which methods are required for every backend.
    - Add optional capability flags for camera, lidar, and state feedback.
    - Add consistent exception types for connection and command failures.
    """

    @abstractmethod
    def connect(self) -> None:
        """Connect to the backend."""

    @abstractmethod
    def set_body_velocity(self, forward_mps: float, turn_radps: float) -> None:
        """Command body velocity."""

    @abstractmethod
    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> None:
        """Command wheel speeds in left, right order."""

    @abstractmethod
    def read_state(self) -> QBotState:
        """Return latest backend state."""

    @abstractmethod
    def stop(self) -> None:
        """Stop movement."""

    @abstractmethod
    def close(self) -> None:
        """Close backend resources."""
