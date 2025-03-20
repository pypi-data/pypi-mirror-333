#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Implements a storage class to write text data to a S3 backend in blocks"""

import io
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

from minio import Minio
from minio.commonconfig import ENABLED, Filter
from minio.lifecycleconfig import LifecycleConfig, Rule, Expiration

logger = logging.getLogger()


class Block(io.BytesIO):
    """Represents a block of data with a given duration"""

    def __init__(self, duration, *args, **kwargs):
        self.start = datetime.now(timezone.utc)
        self.duration = duration
        logger.info(
            "Start new block with start date %s and duration %s",
            self.start,
            self.duration,
        )
        super().__init__(*args, **kwargs)

    def expired(self):
        """Returns if the block duration is exhausted"""
        return self.start + self.duration < datetime.now(timezone.utc)


class Storage:
    """
    A storage class automatically slicing the data into blocks
    of n minutes and storing them on a S3 backend
    """

    def __init__(
        self, bucket: str, prefix: str, client: Minio, duration=timedelta(minutes=5)
    ):
        self._minio_client = client
        self.bucket = bucket
        self.current_block: Optional[Block] = None
        self.prefix = prefix
        self.duration = duration
        self.num_bytes_written = 0
        self._init_bucket()

    def __enter__(self):
        self.current_block = Block(self.duration)
        return self

    def __exit__(self, *args):
        if self.current_block:
            block = self.current_block
            self._complete_current_block(block)
            self.current_block = None

    def _init_bucket(self):
        if not self._minio_client.bucket_exists(self.bucket):
            logger.debug("Create bucket %s", self.bucket)
            self._minio_client.make_bucket(self.bucket)
        logger.debug("Set bucket lifetime")
        self._minio_client.set_bucket_lifecycle(
            self.bucket,
            LifecycleConfig(
                [
                    Rule(
                        ENABLED,
                        expiration=Expiration(days=1),
                        rule_filter=Filter(prefix=""),
                    )
                ]
            ),
        )

    def _complete_current_block(self, block):
        block.seek(io.SEEK_SET, 0)
        timestamp = datetime.now(timezone.utc)
        size = len(block.getvalue())

        if size == 0:
            logger.info("Discarding empty block %s", block.start)
            return

        logger.info("Write block %s", block.start)
        self._minio_client.put_object(
            self.bucket,
            f"{self.prefix}/{timestamp.year}/{timestamp.month:02d}/{timestamp.day:02d}/"
            f"{timestamp.isoformat()}.json",
            block,
            size,
            content_type="application/json",
        )

    def write_line(self, line: str):
        """
        Write a line to the current block.
        If the block is expired it will be written to the next block.
        """
        if self.current_block.expired():
            logger.debug("Current block is expired, complete block and start new")
            block = self.current_block
            self.current_block = None
            self._complete_current_block(block)
            self.current_block = Block(self.duration)

        data = line.encode() + b"\n"
        self.current_block.write(data)
        self.num_bytes_written += len(data)
