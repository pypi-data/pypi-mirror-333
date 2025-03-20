#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""TCP Stream"""
import socket

from ._socket import SocketStream


class TCPStream(SocketStream):
    """TCP Stream"""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        super().__init__()

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((self.host, self.port))
        except OSError as ex:
            raise ConnectionError(
                f"Could not connect to {self.host}:{self.port}"
            ) from ex

        super().open()

    def _read(self, length):
        # On Windows, we cannot use os.read to read from sockets
        return self.sock.recv(length)
