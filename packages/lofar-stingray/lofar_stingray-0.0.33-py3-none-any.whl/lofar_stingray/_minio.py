#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Reusable MinIO helpers"""

import os
from argparse import ArgumentParser, Namespace

from minio import Minio


def add_minio_argument(parser: ArgumentParser):
    """Add minio endpoint argument"""
    parser.add_argument(
        "--endpoint",
        type=str,
        help="the S3 endpoint to use",
        default="s3.service.consul:9000",
    )
    parser.add_argument("--secure", action="store_true")


def get_minio_client(args: Namespace) -> Minio:
    """Create minio client from ENV and args"""
    return Minio(
        args.endpoint,
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
        secure=args.secure,
    )
