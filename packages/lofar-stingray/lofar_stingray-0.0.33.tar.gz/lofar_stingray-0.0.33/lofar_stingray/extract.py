#  Copyright (C) 2025 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Entry point to extract statistic matrices & metadata to store them as HDF5"""

import argparse
import logging
import os
import sys
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlparse

from lofar_station_client.file_access import create_hdf5
from lofar_station_client.statistics.statistics_data import StatisticsDataFile

from lofar_stingray._logging import setup_logging_handler
from lofar_stingray._minio import add_minio_argument, get_minio_client
from lofar_stingray.annotator import XstAnnotator, SstAnnotator, BstAnnotator
from lofar_stingray.reader import S3PacketLoader
from lofar_stingray.utils.argparse import (
    str_lower,
    datetime_from_iso_format_with_tz,
    kv_dict,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(setup_logging_handler())

# Maximum amount of time we look back for metadata:
#   * 10 minutes to guarantee including a periodic dump
#     (in case the metadata is not dumped at the beginning
#      of the observation somehow)
#   * 30 seconds for the lead time (the time at which
#     the metadata actually changes)
MAX_METADATA_LOOKBACK = timedelta(minutes=10, seconds=30)


def _create_parser():
    """Define the parser"""
    parser = argparse.ArgumentParser(
        description="Extract statistics matrices from an S3 bucket into an HDF5 file."
    )
    parser.add_argument("station", type=str_lower, help="the name of the station")
    parser.add_argument(
        "antennafield",
        type=str_lower,
        choices=["lba", "hba", "hba0", "hba1"],
        help="the name of the antenna field",
    )
    parser.add_argument(
        "type",
        type=str_lower,
        choices=["xst", "sst", "bst"],
        help="the type of the statistics",
    )
    parser.add_argument("begin", type=datetime_from_iso_format_with_tz)
    parser.add_argument("end", type=datetime_from_iso_format_with_tz)
    parser.add_argument(
        "source",
        type=urlparse,
        help="the source bucket location of the data",
    )
    parser.add_argument("destination", type=urlparse, help="the destination HDF5 file")
    parser.add_argument(
        "--user-metadata",
        type=kv_dict,
        required=False,
        help="a list of key-value sets to append to the S3 object user metadata",
        metavar="KEY=VAL,KEY=VAL...",
    )
    add_minio_argument(parser)
    return parser


def _round_datetime_ms(timestamp: datetime) -> datetime:
    """Round the given timestamp to the nearst millisecond."""

    subtract_ms = timestamp.microsecond - round(timestamp.microsecond, -3)
    return timestamp - timedelta(microseconds=subtract_ms)


def main(sys_args=None) -> int:
    """Parser main method"""
    logger.debug("Starting hdf5 converter")

    parser = _create_parser()
    args = parser.parse_args(sys_args)
    minio_client = get_minio_client(args or sys.argv[1:])
    logger.info("Using source %s", args.source)

    # connect to storage
    metadata_storage = S3PacketLoader(
        args.source.netloc,
        f"{args.station}/metadata",
        minio_client,
    )

    statistics_storage = S3PacketLoader(
        args.source.netloc,
        f"{args.station}/{args.type}/{args.antennafield}",
        minio_client,
    )

    # wait for metadata to arrive at S3.
    logger.info("Waiting for metadata to arrive on S3 for %s", args.begin)
    if not metadata_storage.wait_for_filenames_after(args.begin):
        logger.error("Metadata not available on S3")

    # wait for data to arrive at S3.
    logger.info("Waiting for statistics to arrive on S3 for %s", args.end)
    if not statistics_storage.wait_for_filenames_after(args.end):
        logger.error("Statistics not available on S3")
        return 1  # this is fatal

    # combine matrices with metadata
    annotator_args = (
        args.station,
        args.antennafield,
        metadata_storage.load_json(args.begin - MAX_METADATA_LOOKBACK, args.end, "ts"),
        statistics_storage.load_json(args.begin, args.end),
    )

    if args.type == "sst":
        annotator = SstAnnotator(*annotator_args)
    elif args.type == "xst":
        annotator = XstAnnotator(*annotator_args)
    else:
        annotator = BstAnnotator(*annotator_args)

    tf = (
        tempfile.NamedTemporaryFile(delete=False)  # pylint: disable=consider-using-with
        if args.destination.scheme != "file"
        else args.destination.geturl()[7:]
    )

    with create_hdf5(tf, StatisticsDataFile) as statistics:
        annotator.write(statistics)

    logger.info("Extraction completed.")
    if args.destination.scheme == "s3":
        tf.close()
        logger.info("Uploading to %s", args.destination)
        minio_client.fput_object(
            args.destination.netloc,
            args.destination.path,
            tf.name,
            metadata=args.user_metadata,
        )
        os.unlink(tf.name)
        logger.info("Upload completed for %s", args.destination)

    logger.info("Shutting down.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
