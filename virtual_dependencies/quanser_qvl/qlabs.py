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

    def send_container(self, container: CommModularContainer) -> bool:
        try:
            data = bytearray(struct.pack("<i", 1 + container.containerSize))
            data += bytearray(struct.pack(">BiiiB", 123, container.containerSize, container.classID, container.actorNumber, container.actorFunction))
            data += container.payload
            count = self._stream.send_byte_array(data, len(data))
            if count > 0:
                self._stream.flush()
                return True
        except Exception:
            return False
        return False

    def receive_new_data(self) -> bool:
        count = self._stream.receive(self._readBuffer, self.BUFFER_SIZE)
        while count > 0:
            self._receivePacketBuffer += bytearray(self._readBuffer[0:count])
            count = self._stream.receive(self._readBuffer, self.BUFFER_SIZE)
        if len(self._receivePacketBuffer) <= 5:
            return False
        if self._receivePacketBuffer[4] != 123:
            self._receivePacketBuffer = bytearray()
            self._receivePacketContainerIndex = 0
            return False
        self._receivePacketSize, = struct.unpack("<I", self._receivePacketBuffer[0:4])
        self._receivePacketSize += 4
        if len(self._receivePacketBuffer) >= self._receivePacketSize:
            self._receivePacketContainerIndex = 5
            return True
        return False

    def get_next_container(self):
        container = CommModularContainer()
        more = False
        index = self._receivePacketContainerIndex
        if index > 0:
            container.containerSize, = struct.unpack(">I", self._receivePacketBuffer[index:index + 4])
            container.classID, = struct.unpack(">I", self._receivePacketBuffer[index + 4:index + 8])
            container.actorNumber, = struct.unpack(">I", self._receivePacketBuffer[index + 8:index + 12])
            container.actorFunction = self._receivePacketBuffer[index + 12]
            start = index + container.BASE_CONTAINER_SIZE
            end = index + container.containerSize
            container.payload = bytearray(self._receivePacketBuffer[start:end])
            self._receivePacketContainerIndex += container.containerSize
            if self._receivePacketContainerIndex >= self._receivePacketSize:
                if len(self._receivePacketBuffer) == self._receivePacketSize:
                    self._receivePacketBuffer = bytearray()
                else:
                    self._receivePacketBuffer = self._receivePacketBuffer[self._receivePacketContainerIndex:]
                self._receivePacketContainerIndex = 0
            else:
                more = True
        return container, more

    def wait_for_container(self, class_id: int, actor_number: int, function_number: int):
        start_time = time.time()
        while True:
            while not self.receive_new_data():
                if self._wait_for_container_timeout > 0:
                    if time.time() - start_time >= self._wait_for_container_timeout:
                        return None
            more = True
            while more:
                container, more = self.get_next_container()
                if container.classID == class_id and container.actorNumber == actor_number and container.actorFunction == function_number:
                    return container

    def flush_receive(self) -> None:
        try:
            self._stream.receive(self._readBuffer, self.BUFFER_SIZE)
        except Exception:
            pass
        self._receivePacketBuffer = bytearray()
        self._receivePacketContainerIndex = 0
