#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""utils to parse argparse arguments"""
from datetime import datetime, timezone


def datetime_from_iso_format_with_tz(datetime_str: str) -> datetime:
    """Parse the given string as an ISO datetime format. Add a default timezone
    if none is provided."""
    dt = datetime.fromisoformat(datetime_str)

    # add timezone if none is provided
    return dt.replace(tzinfo=dt.tzinfo or timezone.utc).astimezone(timezone.utc)


def kv_dict(kv_str: str) -> dict:
    """Parses the given string as a key=val format and returns it as a dict."""
    data = {}
    for kv in kv_str.split(","):
        k, v = kv.split("=", 1)
        data[k] = v
    return data


def str_lower(in_str: str) -> str:
    """Returns given string in lowercase."""
    return in_str.lower()
