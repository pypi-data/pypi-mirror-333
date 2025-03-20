#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Create receiver based on uri"""

import os
from typing import Optional
from urllib.parse import urlsplit

from minio import Minio

from ._file import FileStream
from ._tcp import TCPStream
from ._udp import UDPStream
from ._zmq import ZeroMQReceiver
from ._s3 import StorageStream


def create(uri, writer=False, minio_client: Optional[Minio] = None):
    """Create a Stream based on the given URI"""
    parsed = urlsplit(uri)
    if parsed.scheme == "tcp":
        return TCPStream(parsed.hostname, parsed.port)
    if parsed.scheme == "udp":
        return UDPStream(parsed.hostname, parsed.port, writer)
    if parsed.scheme == "file":
        return FileStream(
            parsed.path, os.O_WRONLY | os.O_CREAT if writer else os.O_RDONLY
        )
    if parsed.scheme == "s3":
        return StorageStream(parsed.netloc, parsed.path, minio_client)
    if parsed.scheme.startswith("zmq"):
        if writer:
            raise ValueError(f"Provided uri '{uri}' is not supported for writing")
        return ZeroMQReceiver(
            f"{parsed.scheme[4:]}://{parsed.netloc}", [parsed.path[1:]]
        )

    raise ValueError(f"Provided uri '{uri}' is not supported")
