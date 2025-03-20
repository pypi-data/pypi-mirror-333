#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Class to aggregate BST statistics"""

import numpy as np
from lofar_station_client.dts.constants import N_pol
from ._base import BaseAggregator
from .message import BSTMessage


class BstAggregator(BaseAggregator):
    """Class to aggregate BST statistics"""

    # beamlets = 488 * 2 for the x and y polarisations
    MAX_BEAMLETS = 488

    def new_matrix(self):
        return np.zeros(
            (self.MAX_BEAMLETS, N_pol),
            dtype=np.float32,
        )

    def add_packet_to_matrix(self, packet, matrix):
        beamlets = packet["payload"]
        nr_beamlets = beamlets.shape[0]
        first_beamlet = packet["data_id"]["beamlet_index"]
        last_beamlet = first_beamlet + nr_beamlets

        # determine which input this packet contains data for
        if last_beamlet > self.MAX_BEAMLETS:
            # packet describes an input that is out of bounds for us
            raise ValueError(
                f"Packet describes {nr_beamlets} beamlets starting at "
                f"{first_beamlet}, but we are limited "
                f"to describing MAX_BEAMLETS={self.MAX_BEAMLETS}"
            )

        matrix[first_beamlet:last_beamlet] = beamlets

        return matrix

    @staticmethod
    def matrix_to_messages(matrix) -> list[BSTMessage]:
        return [BSTMessage(bst_data=matrix)]
