#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Classes to encode ZMQ message payloads."""

from dataclasses import dataclass, asdict, field
from datetime import datetime
import json

import numpy

from lofar_stingray.utils import StingrayJsonEncoder


@dataclass
class Message:
    """Structure to hold the fields for a message to be exchanged over ZMQ."""

    def zmq_payload(self) -> str:
        """Turn this object into a ZMQ message payload."""
        return json.dumps(asdict(self), cls=StingrayJsonEncoder)


@dataclass
# pylint: disable=too-many-instance-attributes
class StatisticsHeader:
    """Generic fields for metadata regarding statistics."""

    # timing information
    timestamp: datetime = datetime.min
    integration_interval: float = 0.0

    # frequency information
    source_info: dict = field(default_factory=dict)
    f_adc: int = 0

    # source of statistics
    station: str = ""
    antenna_field: str = ""
    type: str = ""
    station_id: int = 0
    station_info: dict = field(default_factory=dict)

    # packet header metadata
    packet_version: int = 0
    observation_id: int = 0


@dataclass
class BSTMessage(Message, StatisticsHeader):
    """A message describing and containing BSTs."""

    bst_data: numpy.ndarray = field(default_factory=numpy.array)


@dataclass
class SSTMessage(Message, StatisticsHeader):
    """A message describing and containing SSTs."""

    sst_data: numpy.ndarray = field(default_factory=numpy.array)


@dataclass
class XSTMessage(Message, StatisticsHeader):
    """A message describing and containing XSTs."""

    subband: int = -1
    xst_data_real: numpy.ndarray = field(default_factory=numpy.array)
    xst_data_imag: numpy.ndarray = field(default_factory=numpy.array)
