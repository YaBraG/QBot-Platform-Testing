"""Small QLabs actor base layer."""

from __future__ import annotations

import math
import struct

from virtual_dependencies.quanser_qvl.qlabs import CommModularContainer


class QLabsActor:
    """Base actor class with only the spawn functions this project needs."""

    actorNumber = None
    classID = 0

    def __init__(self, qlabs, verbose: bool = False) -> None:
        self._qlabs = qlabs
        self._verbose = verbose

    def _is_actor_number_valid(self) -> bool:
        return self.actorNumber is not None

    def spawn_id(
        self,
        actorNumber: int,
        location=None,
        rotation=None,
        scale=None,
        configuration: int = 0,
        waitForConfirmation: bool = True,
    ) -> int:
        if location is None:
            location = [0.0, 0.0, 0.0]
        if rotation is None:
            rotation = [0.0, 0.0, 0.0]
        if scale is None:
            scale = [1.0, 1.0, 1.0]

        container = CommModularContainer()
        container.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        container.actorNumber = 0
        container.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID
        container.payload = bytearray(
            struct.pack(
                ">IIfffffffffI",
                self.classID,
                actorNumber,
                location[0],
                location[1],
                location[2],
                rotation[0],
                rotation[1],
                rotation[2],
                scale[0],
                scale[1],
                scale[2],
                configuration,
            )
        )
        container.containerSize = container.BASE_CONTAINER_SIZE + len(container.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if not self._qlabs.send_container(container):
            return -1

        if not waitForConfirmation:
            self.actorNumber = actorNumber
            return 0

        response = self._qlabs.wait_for_container(
            CommModularContainer.ID_GENERIC_ACTOR_SPAWNER,
            0,
            CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID_ACK,
        )
        if response is None or len(response.payload) != 1:
            return -1

        status, = struct.unpack(">B", response.payload[0:1])
        if status == 0:
            self.actorNumber = actorNumber
        return int(status)

    def spawn_id_degrees(
        self,
        actorNumber: int,
        location=None,
        rotation=None,
        scale=None,
        configuration: int = 0,
        waitForConfirmation: bool = True,
    ) -> int:
        if rotation is None:
            rotation = [0.0, 0.0, 0.0]
        rotation_rad = [
            rotation[0] / 180.0 * math.pi,
            rotation[1] / 180.0 * math.pi,
            rotation[2] / 180.0 * math.pi,
        ]
        return self.spawn_id(actorNumber, location, rotation_rad, scale, configuration, waitForConfirmation)
