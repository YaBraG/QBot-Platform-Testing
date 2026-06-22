"""Small QLabs dependency layer used by the virtual QBot backend."""

from virtual_dependencies.quanser_qvl.qlabs import CommModularContainer, QuanserInteractiveLabs
from virtual_dependencies.quanser_qvl.qbot_platform import QLabsQBotPlatform

__all__ = ["CommModularContainer", "QLabsQBotPlatform", "QuanserInteractiveLabs"]
