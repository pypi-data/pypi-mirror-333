#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Provide classes to read data from storage backends"""

from ._s3_packet_loader import S3PacketLoader

__all__ = ["S3PacketLoader"]
