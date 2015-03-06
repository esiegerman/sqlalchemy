"""Import stub for mock library.
"""
from __future__ import absolute_import
from ..util import py33
from nose import SkipTest

if py33:
    from unittest.mock import MagicMock, Mock, call
else:
    try:
        from mock import MagicMock, Mock, call
    except ImportError:
        raise SkipTest(
                "Test requires the 'mock' library")

