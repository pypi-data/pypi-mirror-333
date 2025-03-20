#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Stingray application that transforms statistics packets into matrices,
which are published through ZMQ."""

import argparse
import logging
import queue
import sys
import time
from typing import Dict, Generator

from lofar_station_client.zeromq.publisher import ZeroMQPublisher
from lofar_station_client.statistics.packets import StatisticsPacket
from prometheus_client import start_http_server, disable_created_metrics, Counter, Gauge

from lofar_stingray import streams
from lofar_stingray._logging import setup_logging_handler
from lofar_stingray._prometheus import add_prometheus_argument
from lofar_stingray.aggregator import (
    BstAggregator,
    SstAggregator,
    XstAggregator,
    CollectPacketsPerTimestamp,
)
from lofar_stingray.aggregator.message import Message

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(setup_logging_handler())


def nr_signal_inputs(antenna_field: str):
    """Return the number of SDP signal inputs for the antenna fields."""
    match antenna_field:
        case "hba":
            return 96
        case "hba0":
            return 48
        case "hba1":
            return 48
        case "lba":
            return 192


def first_signal_input_index(antenna_field: str):
    """Return the index of the first signal input in the statistics packets from SDP."""
    match antenna_field:
        case "hba":
            return 0
        case "hba0":
            return 0
        case "hba1":
            return 48
        case "lba":
            return 0


def packets_to_messages(
    station: str, antenna_field: str, mode: str, packets: list[StatisticsPacket]
) -> list[Message]:
    """Convert a set of packages into one or more message payloads for ZMQ"""

    if mode == "sst":
        aggregator = SstAggregator(
            nr_signal_inputs=nr_signal_inputs(antenna_field),
            first_signal_input_index=first_signal_input_index(antenna_field),
        )
    elif mode == "xst":
        aggregator = XstAggregator(
            nr_signal_inputs=nr_signal_inputs(antenna_field),
            first_signal_input_index=first_signal_input_index(antenna_field),
        )
    else:
        aggregator = BstAggregator()

    # combine packets into a matrix
    matrix = aggregator.packets_to_matrix([dict(packet) for packet in packets])
    messages = aggregator.matrix_to_messages(matrix)

    # add header
    packet = packets[0]
    for m in messages:
        m.timestamp = packet.timestamp

        m.station = station
        m.antenna_field = antenna_field
        m.type = mode

        # convert to dict to get all subfields as well
        header_fields = {field[0]: field[1] for field in packet.header}

        m.packet_version = header_fields["version_id"]
        m.station_id = header_fields["station_id"]
        m.station_info = header_fields["station_info"]
        m.source_info = header_fields["source_info"]
        m.f_adc = header_fields["f_adc"]
        m.observation_id = header_fields["observation_id"]
        m.integration_interval = header_fields["integration_interval"]

    return messages


def read_packets(
    stream: streams.Stream, metric_labels: Dict[str, str]
) -> Generator[StatisticsPacket, None, None]:
    """Generator returning all packets read from the given stream until EOF."""

    metric_labels_keys = list(metric_labels.keys())

    metric_nr_bytes_received = Gauge(
        "nr_bytes_received", "Number of bytes received", metric_labels_keys
    ).labels(**metric_labels)
    metric_nr_packets_received = Counter(
        "nr_packets_received",
        "Number of packets received and decoded, per FPGA (or -1 if FPGA is unknown)",
        metric_labels_keys + ["fpga"],
    )
    metric_nr_payload_errors = Counter(
        "nr_payload_errors",
        "Number of packets that were marked by the FPGA for having a payload error",
        metric_labels_keys + ["fpga"],
    )
    metric_nr_decoding_errors = Counter(
        "nr_decoding_errors",
        "Number of packets that could not be decoded as a valid statistics packet",
        metric_labels_keys,
    ).labels(**metric_labels)

    # provide a value to make the metric already available
    metric_nr_bytes_received.inc(0)
    metric_nr_packets_received.labels(**metric_labels, fpga=-1).inc(0)
    metric_nr_payload_errors.labels(**metric_labels, fpga=-1).inc(0)
    metric_nr_decoding_errors.inc(0)

    while True:
        try:
            packet = stream.get_packet()
        except EOFError:
            return
        except ValueError:
            metric_nr_packets_received.labels(**metric_labels, fpga=-1).inc()
            metric_nr_decoding_errors.inc()
            continue
        finally:
            metric_nr_bytes_received.set(stream.num_bytes_read)

        metric_nr_packets_received.labels(
            **metric_labels, fpga=packet.header.gn_index
        ).inc()

        if packet.header.payload_error:
            metric_nr_payload_errors.labels(
                **metric_labels, fpga=packet.header.gn_index
            ).inc()
            continue

        yield packet


def _create_parser():
    """Define the parser"""
    parser = argparse.ArgumentParser(
        description="Records a stream of statistics"
        " packets and publish them as matrices on ZMQ."
    )
    parser.add_argument("station", type=str.lower, help="the station name")
    parser.add_argument(
        "antenna_field",
        type=str.lower,
        choices=["lba", "hba", "hba0", "hba1"],
        help="the antenna-field name",
    )
    parser.add_argument(
        "type",
        type=str.lower,
        choices=["bst", "sst", "xst"],
        help="the type of statistic to write",
    )
    parser.add_argument("source", type=str, help="source of the packets")
    parser.add_argument(
        "--port", type=int, default=6001, help="the ZMQ port number to publish on"
    )
    add_prometheus_argument(parser)
    return parser


def send_message(publisher: ZeroMQPublisher, message) -> bool:
    """Send one message over the ZMQ bus. Return whether
    emission was succesful."""

    try:
        publisher.send(message.zmq_payload())
        return True
    except queue.Full:
        logger.warning("Could not post message: queue is full")
        return False


def main(argv=None):
    """Parser main method"""
    logger.debug("Starting statistics matrix publisher")
    parser = _create_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    # start prometheus server
    disable_created_metrics()
    start_http_server(args.metrics_port)

    # initialise metrics
    metric_labels = {
        "antenna_field": args.antenna_field,
        "type": args.type,
    }

    metric_nr_messages_constructed = Counter(
        "nr_messages_constructed",
        "Number of messages constructed ZMQ",
        list(metric_labels.keys()),
    ).labels(**metric_labels)
    metric_nr_messages_constructed.inc(0)

    metric_nr_messages_published = Counter(
        "nr_messages_published",
        "Number of messages published on ZMQ",
        list(metric_labels.keys()),
    ).labels(**metric_labels)
    metric_nr_messages_published.inc(0)

    # start publishing
    zmq_url = f"tcp://*:{args.port}"
    topic = f"{args.type}/{args.antenna_field}/{args.station}"
    logger.info("Publishing on %s with topic %s", zmq_url, topic)

    with ZeroMQPublisher(zmq_url, [topic]) as publisher:
        logger.info("Waiting for publisher to start...")
        while not publisher.is_running:
            time.sleep(1)

        logger.info("Publisher started")

        collector = CollectPacketsPerTimestamp()

        # processor function for each timestamp
        def process_packets(packets):
            for message in packets_to_messages(
                args.station, args.antenna_field, args.type, packets
            ):
                metric_nr_messages_constructed.inc()
                if send_message(publisher, message):
                    metric_nr_messages_published.inc()

        try:
            # process stream
            with streams.create(args.source) as stream:
                for packet in read_packets(stream, metric_labels):
                    for packets_of_same_timestamp in collector.put_packet(packet):
                        process_packets(packets_of_same_timestamp)

            # process remainder
            for packets_of_same_timestamp in collector.done():
                process_packets(packets_of_same_timestamp)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("Caught exception while processing packets")

    logger.info("End of packet stream. Shutting down.")


if __name__ == "__main__":
    main()
