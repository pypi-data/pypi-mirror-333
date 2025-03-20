#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0


"""Collect statistics packets per timestamp."""

from typing import Generator

from lofar_station_client.statistics.packets import StatisticsPacket


class CollectPacketsPerTimestamp:
    """Collect and return packets per timestamp. Assumes packets arrive in order."""

    def __init__(self):
        self.packets: list[StatisticsPacket] = []
        self.current_timestamp = None

    def put_packet(
        self, packet: StatisticsPacket
    ) -> Generator[list[StatisticsPacket], None, None]:
        """Add another packet. Yield the full set of packets having the same
        timestamp."""

        if packet.timestamp != self.current_timestamp:
            # packet is for next matrix, so current one is complete
            if self.packets:
                yield self.packets
                self.packets = []

            # collect next matrix
            self.current_timestamp = packet.timestamp

        # add to current matrix
        self.packets.append(packet)

    def done(self):
        """Process any remaining data."""

        if self.packets:
            yield self.packets
            self.packets = []
