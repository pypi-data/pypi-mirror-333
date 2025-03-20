#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Reusable logging helpers"""

import logging

from logfmter import Logfmter


def setup_logging_handler():
    """Create a logfmter based logging handler"""
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = Logfmter(
        keys=["ts", "level", "file", "line", "function"],
        mapping={
            "ts": "asctime",
            "level": "levelname",
            "function": "funcName",
            "file": "filename",
            "line": "lineno",
        },
    )
    handler.setFormatter(formatter)
    return handler
