#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""UDP Stream"""
import socket
import logging

from lofar_station_client.statistics.packets import StatisticsPacket

from ._socket import SocketStream

logger = logging.getLogger()

# Maximum size of an Ethernet Jumbo frame
MAX_ETH_FRAME_SIZE = 9000


class UDPStream(SocketStream):
    """UDP Stream"""

    POLL_TIMEOUT = 0.1
    RECV_BUFFER_SIZE = 16 * 1024 * 1024

    def __init__(
        self,
        host,
        port,
        writer: bool = False,
    ):
        self.host = host
        self.port = port
        self.writer = writer
        super().__init__()

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Allow binding even if there are still lingering packets in the kernel for a
        # previous listener that already died. If not, we get an
        # "Address already in use". This is stock socket usage.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Increase buffers to prevent data loss when our class isn't listening.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.RECV_BUFFER_SIZE)

        # Check whether OS could increase buffer. NB: The kernel typically doubles
        # the requested size to account for bookkeeping overhead,
        # see https://linux.die.net/man/7/socket
        actual_recv_buffer_size = self.sock.getsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF
        )

        if actual_recv_buffer_size < self.RECV_BUFFER_SIZE:
            # Typically this is the host OS not allowing us to allocate buffers
            # of this size. Try increasing it using (as root):
            #     sysctl -w net.core.rmem_max=$((16*1024*1024))
            logger.error(
                "OS does not allow requested buffer size. "
                "This could result in UDP packet loss. "
                "Requested %s bytes, got %s. Verify "
                'if "sysctl net.core.rmem_max" is sufficiently large.',
                self.RECV_BUFFER_SIZE,
                actual_recv_buffer_size,
            )

        # specify what host and port to listen on
        if self.writer:
            self.sock.connect((self.host, self.port))
        else:
            self.sock.bind((self.host, self.port))

        # Make sure we can stop receiving packets even if none arrive.
        # Without this, the recvmsg() call blocks indefinitely if no packet arrives.
        self.sock.settimeout(self.POLL_TIMEOUT)

        super().open()

    def read_data(self, data_length) -> bytes:
        # On Windows, we cannot use os.read to read from sockets
        (data, _ancdata, _msg_flags, _address) = self.sock.recvmsg(data_length)
        self.num_bytes_read += len(data)

        return data

    def read_message(self) -> bytes:
        """Read one datagram from UDP and return its payload."""

        while True:
            try:
                return self.read_data(MAX_ETH_FRAME_SIZE)
            except TimeoutError:
                pass

    def get_packet(self) -> StatisticsPacket:
        # A packet is equal to one UDP datagram
        data = self.read_message()
        return StatisticsPacket.parse_packet(data)
