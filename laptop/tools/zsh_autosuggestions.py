# -*- coding: utf-8 -*-

"""
Zsh Autosuggestions Plugin Installation

This module handles the installation of zsh-autosuggestions, which suggests
commands as you type based on history and completions.

Official repository: https://github.com/zsh-users/zsh-autosuggestions
"""

from ._zsh_plugin import install_zsh_plugin


def install_zsh_autosuggestions() -> bool:
    """
    Install zsh-autosuggestions plugin.

    This plugin suggests commands as you type based on your command history.
    It provides fish-like autosuggestions for zsh.

    Installation details:
    - Clones to: ~/.zsh/zsh-autosuggestions
    - Sources: ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
    - Adds configuration to .zshrc

    Returns:
        True if installation was performed, False if already installed

    Raises:
        NotImplementedError: If current shell is not zsh
        subprocess.CalledProcessError: If git clone fails

    Example:
        >>> install_zsh_autosuggestions()
        True  # Plugin was installed
    """
    return install_zsh_plugin(
        repo_url="https://github.com/zsh-users/zsh-autosuggestions",
        plugin_name="zsh-autosuggestions",
        source_file="zsh-autosuggestions.zsh",
    )
