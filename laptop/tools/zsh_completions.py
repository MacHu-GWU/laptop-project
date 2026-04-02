# -*- coding: utf-8 -*-

"""
Zsh Completions Plugin Installation

This module handles the installation of zsh-completions, which provides
additional completion definitions for zsh.

Official repository: https://github.com/zsh-users/zsh-completions
"""

from ._zsh_plugin import install_zsh_plugin


def install_zsh_completions() -> bool:
    """
    Install zsh-completions plugin.

    This plugin provides additional completion definitions for many common
    commands that are not included in the default zsh completion system.

    Installation details:
    - Clones to: ~/.zsh/zsh-completions
    - Adds to fpath: fpath=(~/.zsh/zsh-completions/src $fpath)
    - Adds configuration to .zshrc

    Note: Unlike other plugins, this uses fpath instead of sourcing,
    as it's a completion plugin.

    Returns:
        True if installation was performed, False if already installed

    Raises:
        NotImplementedError: If current shell is not zsh
        subprocess.CalledProcessError: If git clone fails

    Example:
        >>> install_zsh_completions()
        True  # Plugin was installed
    """
    return install_zsh_plugin(
        repo_url="https://github.com/zsh-users/zsh-completions",
        plugin_name="zsh-completions",
        fpath_mode=True,  # Use fpath instead of sourcing
    )
