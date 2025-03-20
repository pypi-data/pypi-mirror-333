from __future__ import annotations

from concurrent.futures import Future, ProcessPoolExecutor, as_completed

import pytest

from pysubconverter import config_context, settings, subconverter


@pytest.fixture
def fake_sub():
    return [
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 1",
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 2",
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 3",
    ]


def _convert(arguments: dict[str, str]) -> str:
    with config_context():
        return subconverter(arguments)


def test_subconverter(fake_sub):
    """Convert basic subscripition links to clash format."""
    arguments: dict[str, str] = {
        "target": "clash",
        "url": "|".join(fake_sub),
    }
    result = _convert(arguments)
    assert "proxies" in result
    assert "fake 1" in result
    assert "fake 2" in result
    assert "fake 3" in result


def test_multi_process_convert(fake_sub):
    """Mulit process conversion test."""
    with ProcessPoolExecutor(max_workers=4) as executor:
        f_to_process: dict[Future[str], str] = {}
        for i in range(2):
            arguments = {
                "target": "clash",
                "url": "|".join([f"{sub} process {i}" for sub in fake_sub]),
            }
            f_to_process[executor.submit(_convert, arguments)] = "process " + str(i)

        for f in as_completed(f_to_process):
            result = f.result()
            assert "proxies" in result
            assert f_to_process[f] in result


def test_settings():
    assert "pref" in settings.pref_path
