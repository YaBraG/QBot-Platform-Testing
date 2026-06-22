"""Check that local virtual dependencies import correctly."""

from qvl.qlabs import CommModularContainer, QuanserInteractiveLabs
from qvl.actor import QLabsActor
from qvl.qbot_platform import QLabsQBotPlatform


def main():
    assert CommModularContainer is not None
    assert QuanserInteractiveLabs is not None
    assert QLabsActor is not None
    assert QLabsQBotPlatform is not None
    print("virtual_dependency_check passed")


if __name__ == "__main__":
    main()
