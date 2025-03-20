#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""UDP Stream"""
import socket
import logging

from lofar_station_client.statistics.packets import StatisticsPacket

from ._stream import Stream

logger = logging.getLogger()


class SocketStream(Stream):
    """Abstract Stream modelling a socket."""

    def __init__(self):
        self._fdesc: int = None
        self.sock: socket.socket = None
        super().__init__()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            self._fdesc = None

    def open(self):
        # subclasses should set self.sock
        self._fdesc = self.sock.fileno()

    def put_packet(self, packet: StatisticsPacket):
        # Caller should make sure not to spam this too fast
        # for the receiver to handle.
        self.sock.send(packet.raw)
        self.num_bytes_written += len(packet.raw)

    def reconnect(self):
        """Reconnect to socket"""
        self.close()
        self.open()
        return True

    @property
    def fdesc(self):
        return self._fdesc
