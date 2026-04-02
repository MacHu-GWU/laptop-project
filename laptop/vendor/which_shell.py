# -*- coding: utf-8 -*-

"""
Shell Detection Utility (Lazy-Loaded)

This module provides a robust and lazy-loaded way to detect the *current active shell*
(e.g., zsh, bash, sh) at runtime.

Why this exists
---------------
Detecting the current shell is surprisingly tricky:

1. ``$SHELL`` is NOT reliable:
   - It represents the user's *login shell*, not the currently running shell.
   - Example: You may have `/bin/zsh` as your login shell, but are currently inside bash.

2. ``ps -p $$`` is NOT sufficient in Python:
   - ``$$`` works in shell, but Python runs as a subprocess.
   - You would often get "python" instead of the actual shell.

3. Parent process (PPID) is the most reliable signal:
   - The Python process is usually launched *by the shell*.
   - Inspecting the parent process gives us the actual interactive shell.

4. Edge cases (CI / Docker / subprocess):
   - In some environments, parent process may not be a shell.
   - We fall back to ``$SHELL`` as a secondary signal.

Design goals
------------
- Lazy evaluation (only compute when needed)
- Safe fallback mechanism
- Extensible for additional shells (fish, dash, etc.)
- Minimal overhead

Usage
-----
>>> shell = ShellInfo()
>>> shell.is_zsh
>>> shell.rc_path

This module is intentionally designed similar to runtime detection utilities.
"""

import os
import subprocess
from pathlib import Path
from functools import cached_property


class ShellInfo:
    """
    Detect information about the current shell environment.

    This class uses a lazy-loading pattern (via ``cached_property``)
    to avoid unnecessary system calls unless the information is accessed.

    Detection strategy (priority order):

    1. Inspect parent process (most reliable)
    2. Fallback to environment variable $SHELL
    3. Raise error if unsupported

    Attributes are evaluated once and cached.
    """

    # ----------------------------------------------------------------------
    # Core detection logic
    # ----------------------------------------------------------------------
    def _get_parent_shell(self) -> str:
        """
        Detect shell from parent process.

        Why:
        ----
        The Python process is typically launched from a shell.
        Therefore, the parent process (PPID) is usually the shell.

        Example:
            zsh → python script.py

        In this case:
            os.getppid() → zsh process

        Returns:
            The command name of the parent process (e.g., "zsh", "bash")
        """
        try:
            ppid = os.getppid()
            result = subprocess.run(
                ["ps", "-p", str(ppid), "-o", "comm="],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception:
            return ""

    def _get_shell_from_env(self) -> str:
        """
        Fallback: detect shell from $SHELL.

        Note:
        -----
        This is less reliable because it reflects the login shell,
        not necessarily the current interactive shell.

        Returns:
            Shell path (e.g., "/bin/zsh")
        """
        return os.environ.get("SHELL", "")

    # ----------------------------------------------------------------------
    # Lazy-loaded properties
    # ----------------------------------------------------------------------
    @cached_property
    def shell_name(self) -> str:
        """
        Return the detected shell name.

        Detection order:
        1. Parent process
        2. $SHELL fallback

        Returns:
            A normalized shell name (e.g., "zsh", "bash", "sh")

        Raises:
            NotImplementedError if shell cannot be determined
        """
        shell = self._get_parent_shell()

        if shell:
            return shell

        # fallback
        shell_env = self._get_shell_from_env()
        if shell_env:
            return Path(shell_env).name

        raise NotImplementedError("Unable to determine current shell")

    @cached_property
    def is_zsh(self) -> bool:
        """Return True if current shell is zsh."""
        return self.shell_name.endswith("zsh")

    @cached_property
    def is_bash(self) -> bool:
        """Return True if current shell is bash."""
        return self.shell_name.endswith("bash")

    @cached_property
    def is_sh(self) -> bool:
        """Return True if current shell is sh."""
        return self.shell_name.endswith("sh")

    @cached_property
    def rc_path(self) -> Path:
        """
        Return the corresponding shell RC file path.

        Mapping:
            zsh  -> ~/.zshrc
            bash -> ~/.bashrc
            sh   -> ~/.shrc

        Raises:
            NotImplementedError if shell is unsupported
        """
        if self.is_zsh:
            return Path.home() / ".zshrc"
        elif self.is_bash:
            return Path.home() / ".bashrc"
        elif self.is_sh:
            return Path.home() / ".shrc"
        else:
            raise NotImplementedError(f"Unsupported shell: {self.shell_name}")


# Singleton instance (recommended usage pattern)
shell = ShellInfo()
