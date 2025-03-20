#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""StorageStream"""

import json

from lofar_station_client.statistics.packets import StatisticsPacket

from lofar_stingray.utils import StingrayJsonEncoder
from lofar_stingray.writer import Storage


class StorageStream(Storage):
    """File receiver"""

    def put_packet(self, packet: StatisticsPacket):
        """Write a packet to the stream, encoded as a line of JSON."""
        data = dict(packet)
        self.put_json(data)

    def put_json(self, data: dict):
        """Write a line of text to the stream."""
        self.write_line(json.dumps(data, cls=StingrayJsonEncoder))
