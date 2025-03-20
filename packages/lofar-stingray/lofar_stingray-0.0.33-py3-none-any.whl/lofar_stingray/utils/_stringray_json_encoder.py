#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""additional stingray JSON encoders"""
from datetime import datetime
from json import JSONEncoder

import numpy


class StingrayJsonEncoder(JSONEncoder):
    """Additional json encoders for numpy and datetime"""

    def default(self, o):
        if isinstance(o, numpy.ndarray):
            return o.tolist()
        if isinstance(o, numpy.integer):
            return int(o)
        if isinstance(o, numpy.floating):
            return float(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return JSONEncoder.default(self, o)
