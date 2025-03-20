from __future__ import annotations

from pysubconverter import _core


def test_core_version():
    assert _core.version() != ""
