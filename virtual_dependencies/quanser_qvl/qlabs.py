"""Small QLabs communication layer."""

from __future__ import annotations

import struct
import time

from quanser.communications import PollFlag, Stream, StreamError

try:
    from quanser.common import Timeout
except ImportError:
    from quanser.communications import Timeout


class CommModularContainer:
    ID_GENERIC_ACTOR_SPAWNER = 135
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID = 10
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID_ACK = 11
    ID_UNKNOWN = 0
    BASE_CONTAINER_SIZE = 13

    def __init__(self) -> None:
        self.containerSize = 0
        self.classID = 0
        self.actorNumber = 0
        self.actorFunction = 0
        self.payload = bytearray()


class QuanserInteractiveLabs:
    BUFFER_SIZE = 100000

    def __init__(self) -> None:
        self._stream = None
        self._readBuffer = bytearray(self.BUFFER_SIZE)
        self._receivePacketBuffer = bytearray()
        self._receivePacketSize = 0
        self._receivePacketContainerIndex = 0
        self._wait_for_container_timeout = 5.0

    def open(self, address: str, timeout: float = 10.0) -> bool:
        uri = f"tcpip://{address}:18000"
        self._stream = Stream()
        result = self._stream.connect(uri, True, self.BUFFER_SIZE, self.BUFFER_SIZE)
        if result is False:
            poll_result = 0
            while (poll_result & PollFlag.CONNECT) != PollFlag.CONNECT and timeout > 0:
                try:
                    poll_result = self._stream.poll(Timeout(1), PollFlag.CONNECT)
                except StreamError as exc:
                    if getattr(exc, "error_code", None) == -33:
                        self._stream.close()
                        return False
                    raise
                timeout -= 1
            if (poll_result & PollFlag.CONNECT) != PollFlag.CONNECT:
                self._stream.close()
                return False
        return True

    def close(self) -> None:
        try:
            self._stream.shutdown()
            self._stream.close()
        except Exception:
            pass
