#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Stream base class"""

import os
from abc import ABC, abstractmethod
import json

from lofar_station_client.statistics.packets import StatisticsPacket, StatisticsHeader

from lofar_stingray.utils import StingrayJsonEncoder


class Stream(ABC):
    """Reads data from a file descriptor."""

    HEADER_LENGTH = 32

    def __init__(self):
        self.num_bytes_read: int = 0
        self.num_bytes_written: int = 0

    def __enter__(self):
        """Open the stream as part of a context manager."""
        self.open()
        return self

    def __exit__(self, type_, value, exc):
        """Close the stream as part of a context manager."""
        self.close()
        return False

    def __del__(self):
        # Make sure we don't leak
        self.close()

    def __iter__(self):
        """Iterates over all packets in the stream."""
        return self

    def __next__(self) -> StatisticsPacket:
        """Return next packet."""
        try:
            return self.get_packet()
        except EOFError as exc:
            raise StopIteration from exc

    @property
    @abstractmethod
    def fdesc(self):
        """Provide the file descriptor for the read function"""

    def open(self):
        """Obtain I/O resources. Is reentrant."""

    def close(self):
        """Release I/O resources. Is reentrant."""

    def get_packet(self) -> StatisticsPacket:
        """Read exactly one statistics packet from the stream."""

        # read only the header, to compute the size of the packet
        header_data = self.read_data(self.HEADER_LENGTH)
        header = StatisticsHeader(header_data)

        # read the rest of the packet (payload)
        payload_length = header.expected_size() - len(header_data)
        payload = self.read_data(payload_length)

        # add payload to the header, and return the full packet
        return StatisticsPacket(header, payload)

    def get_json(self) -> dict:
        """Read exactly one JSON element from the stream. Return as dict."""

        # Streams are not required to implement this
        raise NotImplementedError

    def _read(self, length: int) -> bytes:
        """Low-level read function to fetch at most "length" (>1) bytes. Returns
        nothing if there is no data left."""

        data = os.read(self.fdesc, length)
        self.num_bytes_read += len(data)

        return data

    def read_data(self, data_length: int) -> bytes:
        """Read exactly data_length bytes from the stream."""

        data = b""
        while len(data) < data_length:
            # try to read the remainder.
            # NOTE: recv() may return less data than requested, and returns 0
            # if there is nothing left to read (end of stream)
            more_data = self._read(data_length - len(data))
            if not more_data:
                # connection got dropped
                raise EOFError("End of stream")

            data += more_data

        return data

    def write_data(self, data: bytes):
        """Write an amount of data to the stream."""

        os.write(self.fdesc, data)
        self.num_bytes_written += len(data)

    def put_packet(self, packet: StatisticsPacket):
        """Emit a packet."""

        # For most streams, this is in binary
        self.write_data(packet.raw)

    def put_json(self, data: dict):
        """Emit a dict as JSON on the stream."""
        self.write_data(json.dumps(data, cls=StingrayJsonEncoder).encode() + b"\n")
