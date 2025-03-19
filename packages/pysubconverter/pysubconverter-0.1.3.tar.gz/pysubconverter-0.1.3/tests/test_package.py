from __future__ import annotations

from importlib_metadata import version

import pysubconverter as m


def test_version():
    assert version("pysubconverter") == m.__version__
