# -*- coding: utf-8 -*-

"""
Operating System Detection Utility

This module provides a simple and reliable way to detect the current operating
system at runtime using Python's built-in ``sys.platform``.

Why this approach
-----------------
Python exposes ``sys.platform`` as the canonical signal for platform detection.
It is:

- stable across environments
- lightweight (no subprocess or OS calls)
- widely used in production code

Compared to alternatives:
- ``os.name`` is too coarse (e.g., cannot distinguish macOS vs Linux)
- ``platform.system()`` is more verbose without clear benefits here

This module wraps ``sys.platform`` into a small helper class with lazy-loaded
properties for clarity and convenience.

Usage example
-------------
.. code-block:: python

    from this_module import platform_info

    if platform_info.is_macos:
        print("Running on macOS")

    if platform_info.is_linux:
        print("Running on Linux")

Compatibility
-------------
Requires Python 3.9+ (uses functools.cached_property).
"""

import sys
from functools import cached_property


class OSPlatform:
    """
    Detect the current operating system.

    This class uses lazy-loaded properties so values are computed only when
    accessed and cached afterward.

    Note:
        In practice, ``sys.platform`` is already extremely cheap to access.
        The lazy-loading pattern is used here mainly for API clarity rather
        than performance.
    """

    @cached_property
    def platform_name(self) -> str:
        """
        Return the raw value of ``sys.platform``.

        Common values:
            - "win32"   -> Windows
            - "cygwin"  -> Windows-like environment
            - "darwin"  -> macOS
            - "linux"   -> Linux

        This serves as the source of truth for all other checks.
        """
        return sys.platform

    @cached_property
    def is_windows(self) -> bool:
        """
        Return True if running on Windows.

        Note:
            Python reports Windows as "win32" even on 64-bit systems.
            "cygwin" is also treated as Windows for most practical purposes.
        """
        return self.platform_name in {"win32", "cygwin"}

    @cached_property
    def is_macos(self) -> bool:
        """
        Return True if running on macOS.

        Python reports macOS as "darwin".
        """
        return self.platform_name == "darwin"

    @cached_property
    def is_linux(self) -> bool:
        """
        Return True if running on Linux.

        Uses ``startswith`` for slightly better forward compatibility.
        """
        return self.platform_name.startswith("linux")

    @cached_property
    def is_unix_like(self) -> bool:
        """
        Return True for Unix-like systems (Linux or macOS).

        Useful when platform-specific differences do not matter.
        """
        return self.is_linux or self.is_macos


# Singleton instance (recommended usage)
platform_info = OSPlatform()

# Optional compatibility constants (evaluated once at import time)
IS_WINDOWS = platform_info.is_windows
IS_MACOS = platform_info.is_macos
IS_LINUX = platform_info.is_linux