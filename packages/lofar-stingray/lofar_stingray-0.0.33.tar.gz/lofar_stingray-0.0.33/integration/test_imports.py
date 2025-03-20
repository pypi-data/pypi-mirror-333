#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

"""Testing of importing parts of installed package"""

from unittest import TestCase

# pylint: disable=import-outside-toplevel


class ImportTest(TestCase):
    """Test cases for imports"""

    def test_import_version(self):
        """Test importing version string"""
        try:
            from lofar_stingray import __version__
        except ImportError:
            __version__ = None

        self.assertIsNotNone(__version__)
