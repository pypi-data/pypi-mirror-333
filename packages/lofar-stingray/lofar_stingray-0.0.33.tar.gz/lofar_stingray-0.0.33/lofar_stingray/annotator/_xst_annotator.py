#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Class to aggregate XST statistics"""

from datetime import datetime
from typing import Iterable

import numpy

from lofar_station_client.statistics.statistics_data import (
    StatisticsDataFile,
)

from ._base import BaseAnnotator


class XstAnnotator(BaseAnnotator):
    """Class to aggregate XST statistics packets."""

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
        return "XST"

    def write(self, statistics: StatisticsDataFile):
        self.set_file_header(statistics)

        for matrix in self.matrices:
            timestamp = self.round_datetime_ms(
                datetime.fromisoformat(matrix["timestamp"])
            )
            subband = matrix["subband"]

            real = numpy.array(matrix["xst_data_real"], dtype=numpy.float32)
            imag = numpy.array(matrix["xst_data_imag"], dtype=numpy.float32)
            values = real + imag * 1j

            statistics[f"XST_{self.format_timestamp(timestamp)}_SB{subband:03}"] = (
                values
            )
