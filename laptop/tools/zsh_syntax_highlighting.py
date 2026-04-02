# -*- coding: utf-8 -*-

"""
Zsh Syntax Highlighting Plugin Installation

This module handles the installation of zsh-syntax-highlighting, which provides
fish-like syntax highlighting for zsh commands.

Official repository: https://github.com/zsh-users/zsh-syntax-highlighting
"""

from ._zsh_plugin import install_zsh_plugin


def install_zsh_syntax_highlighting() -> bool:
    """
    Install zsh-syntax-highlighting plugin.

    This plugin provides syntax highlighting for zsh commands as you type.
    Valid commands are highlighted in green, invalid ones in red.

    Installation details:
    - Clones to: ~/.zsh/zsh-syntax-highlighting
    - Sources: ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
    - Adds configuration to .zshrc

    Returns:
        True if installation was performed, False if already installed

    Raises:
        NotImplementedError: If current shell is not zsh
        subprocess.CalledProcessError: If git clone fails

    Example:
        >>> install_zsh_syntax_highlighting()
        True  # Plugin was installed
    """
    return install_zsh_plugin(
        repo_url="https://github.com/zsh-users/zsh-syntax-highlighting",
        plugin_name="zsh-syntax-highlighting",
        source_file="zsh-syntax-highlighting.zsh",
    )
