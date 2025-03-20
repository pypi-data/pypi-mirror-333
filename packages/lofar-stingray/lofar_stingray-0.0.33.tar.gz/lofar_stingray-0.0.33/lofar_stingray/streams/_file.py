#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""FileStream"""

import os

from ._stream import Stream


class FileStream(Stream):
    """File receiver"""

    def __init__(self, filename, mode=os.O_RDONLY):
        self.filename = filename
        self.fileno = None
        self.mode = mode
        super().__init__()

    def open(self):
        self.fileno = os.open(self.filename, self.mode)

    def close(self):
        if self.fileno:
            os.close(self.fileno)
            self.fileno = None

    @property
    def fdesc(self):
        return self.fileno
