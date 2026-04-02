# -*- coding: utf-8 -*-

"""
Zsh Autocomplete Plugin Installation

This module handles the installation of zsh-autocomplete, which provides
real-time type-ahead autocompletion for zsh.

Official repository: https://github.com/marlonrichert/zsh-autocomplete
"""

from ._zsh_plugin import install_zsh_plugin


def install_zsh_autocomplete() -> bool:
    """
    Install zsh-autocomplete plugin.

    This plugin provides real-time type-ahead autocompletion for zsh,
    similar to fish shell's behavior. It shows completion suggestions
    as you type and allows immediate selection.

    Installation details:
    - Clones to: ~/.zsh/zsh-autocomplete
    - Sources: ~/.zsh/zsh-autocomplete/zsh-autocomplete.plugin.zsh
    - Adds configuration to .zshrc

    Returns:
        True if installation was performed, False if already installed

    Raises:
        NotImplementedError: If current shell is not zsh
        subprocess.CalledProcessError: If git clone fails

    Example:
        >>> install_zsh_autocomplete()
        True  # Plugin was installed
    """
    return install_zsh_plugin(
        repo_url="https://github.com/marlonrichert/zsh-autocomplete",
        plugin_name="zsh-autocomplete",
        source_file="zsh-autocomplete.plugin.zsh",
    )
