#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""ZeroMQ Receiver"""
import datetime
import json
import logging
from typing import Union, Tuple, List

import zmq

from lofar_station_client.zeromq.subscriber import ZeroMQSubscriber

logger = logging.getLogger()


class ZeroMQReceiver(ZeroMQSubscriber):
    """ZeroMQ Receiver"""

    def __init__(
        self, uri: str, topics: List[str], content_type: str = "application/json"
    ):
        super().__init__(uri, topics)

        # pylint: disable=fixme
        # TODO: pull topics from URI to create fully configurable and routable end point
        self._topics = topics
        self._content_type = content_type

        self.num_bytes_read = 0

    def __iter__(self):
        """Iterates over all packets in the stream."""
        return self

    def read_message(self) -> Tuple[str, datetime.datetime, Union[dict, str, bytes]]:
        """Read a message, and return it as a (topic, timestamp, message) tuple."""
        while True:
            # parse the message according to the format we publish them with
            topic, timestamp, msg = self.recv()
            self.num_bytes_read += len(msg)

            if self._content_type == "application/json":
                return topic, timestamp, json.loads(msg.decode())
            if self._content_type == "text/plain":
                return topic, timestamp, msg.decode()

            return topic, timestamp, msg

    def __next__(self) -> Union[str, bytes]:
        """Read the next message."""
        try:
            _topic, _timestamp, msg = self.read_message()
            return msg
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                raise StopIteration from e
            raise

    def get_json(self) -> dict:
        """Read a message containing a JSON payload,
        returned as a dict, or None if the stream was closed."""
        try:
            _topic, _timestamp, msg = self.read_message()
            return msg
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return None
            raise

    @property
    def content_type(self):
        """Returns the content type of the receiver"""
        return self._content_type
