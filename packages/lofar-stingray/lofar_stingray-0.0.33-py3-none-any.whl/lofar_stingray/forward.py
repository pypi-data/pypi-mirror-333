#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Stingray forwarder application"""

import argparse
import logging
import sys

from prometheus_client import start_http_server, disable_created_metrics, Counter, Gauge

from lofar_stingray import streams
from lofar_stingray._logging import setup_logging_handler
from lofar_stingray._minio import get_minio_client, add_minio_argument
from lofar_stingray._prometheus import add_prometheus_argument

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(setup_logging_handler())


def _create_parser():
    """Define the parser"""
    parser = argparse.ArgumentParser(
        description="Copy a stream of statistics packets or json"
        " (matrices, metadata) from a source to a destination."
    )
    parser.add_argument(
        "source", type=str, help="the source of the data (file, udp, tcp, zmq)"
    )
    parser.add_argument(
        "destination",
        type=str,
        help="the destination location to use (file, udp, tcp, s3)",
    )
    parser.add_argument(
        "-d",
        "--datatype",
        choices=["packet", "json"],
        default="packet",
        help="type of data that is copied",
    )
    add_prometheus_argument(parser)
    add_minio_argument(parser)
    return parser


def main(argv=None):
    """Parser main method"""
    logger.debug("Starting stingray forwarder")
    parser = _create_parser()
    args = parser.parse_args(argv or sys.argv[1:])
    logger.info("Using source %s", args.source)
    logger.info("Using destination %s", args.destination)

    # start prometheus server
    disable_created_metrics()
    start_http_server(args.metrics_port)

    # initialise metrics
    metric_nr_bytes_read = Gauge(
        "nr_bytes_read",
        "Number of bytes read from the input",
    )
    metric_nr_bytes_read.inc(0)
    metric_nr_bytes_written = Gauge(
        "nr_bytes_written",
        "Number of bytes written to the output",
    )
    metric_nr_bytes_written.inc(0)

    metric_nr_packets_processed = Counter(
        "nr_packets_processed",
        "Number of packets read from the input and written to the output",
    )
    metric_nr_packets_processed.inc(0)

    # obtain s3 client, if needed
    if args.destination.startswith("s3:"):
        minio_client = get_minio_client(args)
    else:
        minio_client = None

    with streams.create(args.destination, True, minio_client) as writer:
        with streams.create(args.source, False, minio_client) as reader:
            try:
                if args.datatype == "packet":
                    for packet in reader:
                        writer.put_packet(packet)

                        metric_nr_packets_processed.inc()
                        metric_nr_bytes_read.set(reader.num_bytes_read)
                        metric_nr_bytes_written.set(writer.num_bytes_written)

                elif args.datatype == "json":
                    while data := reader.get_json():
                        writer.put_json(data)

                        metric_nr_packets_processed.inc()
                        metric_nr_bytes_read.set(reader.num_bytes_read)
                        metric_nr_bytes_written.set(writer.num_bytes_written)
            except Exception:  # pylint: disable=broad-exception-caught
                logger.exception("Caught exception while forwarding packets")

    logger.info("End of packet stream. Shutting down.")


if __name__ == "__main__":
    main()
