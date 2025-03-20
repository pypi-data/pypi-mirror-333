#  Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""
A storage class automatically slicing the data into blocks
of n minutes and storing them on a S3 backend
"""

import json
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Generator

import minio.datatypes
from minio import Minio

logger = logging.getLogger()

# Interval with which to check the Minio store for data
MINIO_POLL_INTERVAL = timedelta(seconds=20)

# Delay with which blocks appear on S3 after being generated
# The blocks are synced at 5 minute intervals, and require
# a few seconds to copy.
MAX_BLOCK_SYNC_DELAY = timedelta(minutes=5, seconds=10)


class S3PacketLoader:  # pylint: disable=too-few-public-methods
    """
    A storage class automatically slicing the data into blocks
    of n minutes and storing them on a S3 backend
    """

    def __init__(
        self,
        bucket: str,
        prefix: str,
        client: Minio,
        block_duration: timedelta = timedelta(minutes=5),
    ):
        self._minio_client = client
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        self.block_duration = block_duration

    def _list_objects_after(
        self, timestamp: datetime
    ) -> Generator[minio.datatypes.Object, None, None]:
        """Return a list of objects that (should) contain packets of and after
        the given timestamp."""

        # NB: The timestamp in the filename is the time when the file was
        # completed, so after the last timestamp recorded in the file.
        return self._minio_client.list_objects(
            self.bucket,
            recursive=True,
            prefix=f"{self.prefix}",
            start_after=f"{self.prefix}/{timestamp.year}/{timestamp.month:02d}/"
            f"{timestamp.day:02d}/{timestamp.isoformat()}.json",
        )

    def wait_for_filenames_after(self, timestamp: datetime) -> bool:
        """Wait until filenames with the given timestamp are on disk.

        Returns whether such files were found."""

        # if the packets are there, always return True
        if next(self._list_objects_after(timestamp), False):
            logger.info(
                "wait_for_filenames_after: Requested timestamp are available at startup"
            )
            return True

        # latest timestamp data can arrive
        max_arrival_time = timestamp + self.block_duration + MAX_BLOCK_SYNC_DELAY
        start_time = datetime.now(tz=timestamp.tzinfo)

        # wait for the end block to hit the disk, to make sure all data is there
        while (
            max_wait_time := max_arrival_time - datetime.now(tz=timestamp.tzinfo)
        ) > timedelta(0):
            logger.info(
                "wait_for_filenames_after: Requested timestamp are not available, "
                "will wait at most %s for them",
                max_wait_time,
            )
            # max_delay = max(timedelta(0), max_arrival_time - datetime.now())
            sleep_interval = min(max_wait_time, MINIO_POLL_INTERVAL)
            time.sleep(sleep_interval.seconds)

            if next(self._list_objects_after(timestamp), False):
                logger.info(
                    "wait_for_filenames_after: Requested timestamp appeared "
                    "after waiting %s",
                    datetime.now(tz=timestamp.tzinfo) - start_time,
                )
                return True

        logger.info(
            "wait_for_filenames_after: Requested timestamp are NOT available, "
            "even after waiting for %s",
            datetime.now(tz=timestamp.tzinfo) - start_time,
        )
        return False

    def load_json(self, start: datetime, end: datetime, ts_field="timestamp") -> list:
        """Loads json lines from the S3 storage until no matching packets are found"""

        for obj in self._list_objects_after(start):
            packets = []
            response = None
            stop = False
            try:
                response = self._minio_client.get_object(self.bucket, obj.object_name)

                for line in response:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    packet = json.loads(line)
                    packet_ts = datetime.fromisoformat(packet[ts_field])
                    packet_ts = packet_ts.replace(
                        tzinfo=packet_ts.tzinfo or timezone.utc
                    ).astimezone(timezone.utc)

                    if packet_ts < start:
                        continue
                    if packet_ts > end:
                        stop = True
                        continue
                    packets.append(packet)
            finally:
                response.close()
                response.release_conn()

            if stop and len(packets) == 0:
                return

            yield from packets
