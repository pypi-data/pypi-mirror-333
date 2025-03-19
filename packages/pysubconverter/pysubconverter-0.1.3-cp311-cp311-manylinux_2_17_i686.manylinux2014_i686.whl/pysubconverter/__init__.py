"""
Copyright (c) 2025 l.feng. All rights reserved.

pysubconverter: A wrapper from subconverter
"""

from __future__ import annotations

import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from appdirs import user_cache_dir
from filelock import FileLock
from importlib_metadata import distribution

from pysubconverter._core import (
    flush_cache,
    get,
    get_local,
    get_profile,
    get_ruleset,
    init_config,
    render,
    settings,
    sub_to_clashr,
    subconverter,
    surge_to_clashr,
    update_config,
)

from ._version import version as __version__

__all__ = [
    "__version__",
    "flush_cache",
    "get",
    "get_local",
    "get_profile",
    "get_ruleset",
    "init_config",
    "render",
    "settings",
    "sub_to_clashr",
    "subconverter",
    "surge_to_clashr",
    "update_config",
]


def default_cache_dir() -> str:
    """
    Get the default cache directory for pysubconverter.
    """
    return str(user_cache_dir("pysubconverter"))


@contextmanager
def config_context(
    cache_dir: str = default_cache_dir(),
    renew: bool = False,
) -> Generator[None, Any, None]:
    """
    Context manager for initializing and configuring the config directory with enhanced safety.

    Args:
        cache_dir: Directory path for caching configurations
        renew: Force renew configuration files when True

    Yields:
        None: Context manager protocol

    Raises:
        FileNotFoundError: If package config directory not found
        RuntimeError: If directory operations fail
    """
    config_lock = FileLock(Path(cache_dir) / "config.lock")
    config_dir = Path(cache_dir) / "config"

    with config_lock:
        try:
            pkg_config = distribution(__package__).locate_file(__package__) / "config"
            if not pkg_config.exists():
                raise FileNotFoundError(
                    "Package config directory not found at" + str(pkg_config)
                )

            if renew and config_dir.exists():
                shutil.rmtree(config_dir)

            if not config_dir.exists():
                shutil.copytree(str(pkg_config), config_dir)

            origin_dir = Path.cwd().resolve()
            try:
                os.chdir(config_dir)
                init_config()
                yield
            except Exception as e:
                raise RuntimeError(
                    "Failed to initialize config in " + str(config_dir) + " : " + str(e)
                ) from e
            finally:
                os.chdir(origin_dir)

        except (shutil.Error, OSError) as e:
            raise RuntimeError("Configuration management failed: " + str(e)) from e
