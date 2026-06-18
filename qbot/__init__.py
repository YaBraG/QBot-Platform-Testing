"""Core QBot Platform package.

This package exposes the clean project API. It should not expose raw Quanser
classes directly.

TODO:
- Export QBotMover after the mover API is stable.
- Export QBotState and QBotCommand after the data model is stable.
- Keep this file lightweight so importing qbot does not require Quanser.
"""

__all__: list[str] = []
