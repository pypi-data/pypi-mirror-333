#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Class to aggregate SST statistics"""

import numpy as np
from ._base import BaseAggregator
from .message import SSTMessage


class SstAggregator(BaseAggregator):
    """Class to aggregate SST statistics"""

    # Maximum number of antenna inputs we support (used to determine array sizes)
    MAX_INPUTS = 192

    # Maximum number of subbands we support (used to determine array sizes)
    MAX_SUBBANDS = 512

    def __init__(
        self,
        nr_signal_inputs: int = MAX_INPUTS,
        first_signal_input_index: int = 0,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.nr_signal_inputs = nr_signal_inputs
        self.first_signal_input_index = first_signal_input_index

    def new_matrix(self):
        return np.zeros((self.nr_signal_inputs, self.MAX_SUBBANDS), dtype=np.float32)

    def add_packet_to_matrix(self, packet, matrix):
        # amount of antennas
        input_index = (
            packet["data_id"]["signal_input_index"] - self.first_signal_input_index
        )

        # determine which input this packet contains data for
        if not 0 <= input_index < self.nr_signal_inputs:
            # packet describes an input that is out of bounds for us
            raise ValueError(
                f"Packet describes input {packet['data_id']['signal_input_index']}"
                f", but we are limited to describing {self.nr_signal_inputs}"
                f" starting at index {self.first_signal_input_index}"
            )

        matrix[input_index][: packet["nof_statistics_per_packet"]] = packet["payload"]

        return matrix

    @staticmethod
    def matrix_to_messages(matrix) -> list[SSTMessage]:
        return [SSTMessage(sst_data=matrix)]
