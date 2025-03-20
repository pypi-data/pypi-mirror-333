#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Base annotator class"""


from abc import ABC, abstractmethod

import numpy

from .message import Message


class BaseAggregator(ABC):
    """Base annotator class"""

    def __init__(self):
        pass

    @abstractmethod
    def new_matrix(self):
        """Return an empty matrix into which all packets
        with the same timestamp can be aggregated"""

    @abstractmethod
    def add_packet_to_matrix(self, packet, matrix: numpy.ndarray) -> numpy.ndarray:
        """Add a packet to the matrix. Returns the updated matrix."""

    def packets_to_matrix(self, packets: list):
        """Combine multiple packets into a single matrix."""

        matrix = self.new_matrix()
        for packet in packets:
            if packet["source_info"]["payload_error"]:
                continue

            matrix = self.add_packet_to_matrix(packet, matrix)

        return matrix

    @staticmethod
    @abstractmethod
    def matrix_to_messages(matrix) -> list[Message]:
        """Convert a matrix into one or more dicts."""
