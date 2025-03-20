#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Reusable Prometheus helpers"""

from argparse import ArgumentParser


def add_prometheus_argument(parser: ArgumentParser):
    """Add prometheus endpoint argument"""
    parser.add_argument(
        "--metrics-port",
        type=int,
        default=8000,
        help="the HTTP port number for exposing Prometheus metrics",
    )
