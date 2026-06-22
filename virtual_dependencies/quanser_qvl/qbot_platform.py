"""Small virtual QBot Platform actor layer."""

from __future__ import annotations

import struct

from virtual_dependencies.quanser_qvl.actor import QLabsActor
from virtual_dependencies.quanser_qvl.qlabs import CommModularContainer


class QLabsQBotPlatform(QLabsActor):
    ID_QBOT_PLATFORM = 23
    FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE = 10
    FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE = 11

    def __init__(self, qlabs, verbose: bool = False) -> None:
        super().__init__(qlabs, verbose)
        self.classID = self.ID_QBOT_PLATFORM

    def command_and_request_state(self, rightWheelSpeed, leftWheelSpeed, leftLED=None, rightLED=None):
        if leftLED is None:
            leftLED = [1.0, 0.0, 0.0]
        if rightLED is None:
            rightLED = [1.0, 0.0, 0.0]

        default = (False, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], False, False, False, 0.0, 0.0, 0, 0)
        if not self._is_actor_number_valid():
            return default

        container = CommModularContainer()
        container.classID = self.ID_QBOT_PLATFORM
        container.actorNumber = self.actorNumber
        container.actorFunction = self.FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE
        container.payload = bytearray(struct.pack(">ffffffff", rightWheelSpeed, leftWheelSpeed, leftLED[0], leftLED[1], leftLED[2], rightLED[0], rightLED[1], rightLED[2]))
        container.containerSize = container.BASE_CONTAINER_SIZE + len(container.payload)

        self._qlabs.flush_receive()
        if not self._qlabs.send_container(container):
            return default
        response = self._qlabs.wait_for_container(self.ID_QBOT_PLATFORM, self.actorNumber, self.FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE)
        if response is None or len(response.payload) != 55:
            return default

        values = struct.unpack(">fffffffff???ffII", response.payload[0:55])
        location = [values[0], values[1], values[2]]
        forward = [values[3], values[4], values[5]]
        up = [values[6], values[7], values[8]]
        return True, location, forward, up, values[9], values[10], values[11], values[12], values[13], values[14], values[15]
