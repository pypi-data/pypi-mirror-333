#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Class to aggregate XST statistics"""

import numpy
from lofar_station_client.math.baseline import nr_baselines
from ._base import BaseAggregator
from .message import XSTMessage


class XstAggregator(BaseAggregator):
    """Class to aggregate XST statistics packets."""

    # Maximum number of antenna inputs we support (used to determine array sizes)
    MAX_INPUTS = 192

    # Maximum number of baselines we can receive
    MAX_BASELINES = nr_baselines(MAX_INPUTS)

    # Expected block size is BLOCK_LENGTH x BLOCK_LENGTH
    BLOCK_LENGTH = 12

    # Expected number of blocks: enough to cover all baselines without the conjugates
    # (that is, the top-left triangle of the matrix).
    MAX_BLOCKS = nr_baselines(MAX_INPUTS // BLOCK_LENGTH)

    # Maximum number of subbands we support (used to determine array sizes)
    MAX_SUBBANDS = 512

    # Complex values are (real, imag). A bit silly, but we don't want magical
    # constants.
    VALUES_PER_COMPLEX = 2

    def __init__(
        self,
        nr_signal_inputs=MAX_INPUTS,
        first_signal_input_index=0,
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.nr_signal_inputs = nr_signal_inputs
        self.first_signal_input_index = first_signal_input_index

        super().__init__()

    @property
    def nr_blocks(self):
        """Number of blocks that contain XSTs for our signal inputs."""
        return nr_baselines(self.nr_signal_inputs // self.BLOCK_LENGTH)

    def _validate_baselines(self, first_baseline, nof_signal_inputs):

        # check whether set of baselines in this packet are not out of bounds
        for antenna in (0, 1):
            if not (
                0
                <= first_baseline[antenna]
                + nof_signal_inputs
                - self.first_signal_input_index
                <= self.nr_signal_inputs
            ):
                # packet describes an input that is out of bounds for us
                raise ValueError(
                    f"Packet describes {nof_signal_inputs} x"
                    f"{nof_signal_inputs} baselines starting at"
                    f"{first_baseline}, but we are limited to "
                    f"describing {self.nr_signal_inputs} starting at offset "
                    f"{self.first_signal_input_index}"
                )

            # the blocks of baselines need to be tightly packed, and thus be provided
            # at exact intervals
            if first_baseline[antenna] % self.BLOCK_LENGTH != 0:
                raise ValueError(
                    f"Packet describes baselines starting at "
                    f"{first_baseline}, "
                    f"but we require a multiple of BLOCK_LENGTH={self.BLOCK_LENGTH}"
                )

    def _transpose_block(self, first_baseline, block):
        # Make sure we always have a baseline (a,b) with a>=b. If not, we swap the
        # indices and mark that the data must be conjugated and transposed when
        # processed.

        conjugated = False

        if first_baseline[0] < first_baseline[1]:
            conjugated = True
            first_baseline = (first_baseline[1], first_baseline[0])

        # Adjust for our offset
        first_baseline = (
            first_baseline[0] - self.first_signal_input_index,
            first_baseline[1] - self.first_signal_input_index,
        )

        block = (
            block.astype(numpy.float32)
            .view(numpy.complex64)
            .reshape(self.BLOCK_LENGTH, self.BLOCK_LENGTH)
        )

        if conjugated:
            block = block.conjugate().transpose()
        return first_baseline, block

    def new_matrix(self):
        return numpy.array(
            [],
            dtype=[
                ("subband", numpy.int32),
                (
                    "data",
                    numpy.complex64,
                    (self.nr_signal_inputs, self.nr_signal_inputs),
                ),
            ],
        )

    def add_packet_to_matrix(self, packet, matrix):
        nof_signal_inputs = packet["nof_signal_inputs"]
        first_baseline = packet["data_id"]["first_baseline"]

        if nof_signal_inputs != self.BLOCK_LENGTH:
            raise ValueError(
                f"Packet describes a block of {nof_signal_inputs} x "
                f"{nof_signal_inputs} baselines, but we can only parse "
                f"blocks of {self.BLOCK_LENGTH} x {self.BLOCK_LENGTH} baselines"
            )

        self._validate_baselines(first_baseline, nof_signal_inputs)

        subband = packet["data_id"]["subband_index"]

        block = numpy.zeros(
            (self.BLOCK_LENGTH * self.BLOCK_LENGTH * self.VALUES_PER_COMPLEX)
        )
        block[: packet["nof_statistics_per_packet"]] = packet["payload"]

        first_baseline, block = self._transpose_block(first_baseline, block)

        if subband not in matrix["subband"]:
            matrix = numpy.append(
                matrix,
                numpy.array(
                    [
                        (
                            subband,
                            numpy.zeros(
                                (self.nr_signal_inputs, self.nr_signal_inputs),
                                dtype=numpy.complex64,
                            ),
                        )
                    ],
                    dtype=matrix.dtype,
                ),
            )

        (idx,) = numpy.nonzero(matrix["subband"] == subband)
        matrix[idx[0]]["data"][
            first_baseline[0] : first_baseline[0] + self.BLOCK_LENGTH,
            first_baseline[1] : first_baseline[1] + self.BLOCK_LENGTH,
        ] = block

        return matrix

    @staticmethod
    def matrix_to_messages(matrix) -> list[XSTMessage]:
        return [
            XSTMessage(
                subband=subband,
                xst_data_real=numpy.real(data),
                xst_data_imag=numpy.imag(data),
            )
            for subband, data in matrix
        ]
