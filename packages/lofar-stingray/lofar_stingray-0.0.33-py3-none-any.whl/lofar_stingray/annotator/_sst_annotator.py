#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Class to aggregate SST statistics"""

from datetime import datetime
from typing import Iterable

import numpy

from lofar_station_client.statistics.statistics_data import (
    StatisticsDataFile,
)

from ._base import BaseAnnotator


class SstAnnotator(BaseAnnotator):
    """Class to aggregate SST statistics"""

    def __init__(
        self,
        station: str,
        antennafield: str,
        metadata_packets: Iterable,
        matrices: Iterable,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(station, antennafield, metadata_packets)
        self.matrices = matrices

    @property
    def mode(self):
        return "SST"

    def write(self, statistics: StatisticsDataFile):
        self.set_file_header(statistics)

        for matrix in self.matrices:
            timestamp = self.round_datetime_ms(
                datetime.fromisoformat(matrix["timestamp"])
            )

            values = numpy.array(matrix["sst_data"], dtype=numpy.float32)

            statistics[f"SST_{self.format_timestamp(timestamp)}"] = values
