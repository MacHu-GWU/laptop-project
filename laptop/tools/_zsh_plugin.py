# -*- coding: utf-8 -*-

"""
Common Zsh Plugin Installation Logic

This internal module provides shared functionality for installing zsh plugins
from GitHub repositories. It handles:
- Git cloning to standard locations
- Adding source lines to .zshrc
- Idempotent installation

This module is not meant to be used directly - it's a helper for specific
plugin installation modules.
"""

from __future__ import annotations

from pathlib import Path

from ..utils import git_clone
from ..utils import add_line_to_config
from ..vendor.which_shell import shell


def install_zsh_plugin(
    repo_url: str,
    plugin_name: str,
    source_file: str | None = None,
    fpath_mode: bool = False,
) -> bool:
    """
    Generic function to install a zsh plugin from GitHub.

    This function:
    1. Clones the plugin repository to ~/.zsh/{plugin_name}
    2. Adds the appropriate line to .zshrc:
       - For regular plugins: source ~/.zsh/{plugin_name}/{source_file}
       - For fpath plugins: fpath=(~/.zsh/{plugin_name}/src $fpath)

    Args:
        repo_url: GitHub repository URL (e.g., 'https://github.com/zsh-users/zsh-autosuggestions')
        plugin_name: Name of the plugin (used as directory name)
        source_file: The .zsh file to source (e.g., 'zsh-autosuggestions.zsh')
                     Not needed if fpath_mode=True
        fpath_mode: If True, add to fpath instead of sourcing
                    (used for completion plugins like zsh-completions)

    Returns:
        True if installation was performed, False if plugin was already installed

    Raises:
        ValueError: If source_file is None when fpath_mode is False
        subprocess.CalledProcessError: If git clone fails

    Example:
        >>> # Regular plugin (source mode)
        >>> install_zsh_plugin(
        ...     repo_url="https://github.com/zsh-users/zsh-autosuggestions",
        ...     plugin_name="zsh-autosuggestions",
        ...     source_file="zsh-autosuggestions.zsh",
        ... )

        >>> # Completion plugin (fpath mode)
        >>> install_zsh_plugin(
        ...     repo_url="https://github.com/zsh-users/zsh-completions",
        ...     plugin_name="zsh-completions",
        ...     fpath_mode=True,
        ... )
    """
    if not fpath_mode and source_file is None:
        raise ValueError("source_file is required when fpath_mode=False")

    # Check if we're in zsh (these plugins only work with zsh)
    if not shell.is_zsh:
        raise NotImplementedError(
            f"Zsh plugins can only be installed in zsh shell. "
            f"Current shell: {shell.shell_name}"
        )

    # Define installation paths
    zsh_dir = Path.home() / ".zsh"
    zsh_dir.mkdir(parents=True, exist_ok=True)

    plugin_dir = zsh_dir / plugin_name
    rc_path = shell.rc_path

    # Check if plugin is already installed
    if plugin_dir.exists() and (plugin_dir / ".git").exists():
        print(f"{plugin_name} is already installed at {plugin_dir}, skipping clone...")
        was_cloned = False
    else:
        # Clone the plugin repository
        print(f"Cloning {plugin_name}...")
        was_cloned = git_clone(
            url=repo_url,
            path=plugin_dir,
            depth=1,
            force_reclone=False,
        )

        if was_cloned:
            print(f"{plugin_name} cloned successfully to {plugin_dir}")

    # Add configuration to .zshrc
    comment_line = f"# Enable {plugin_name}"

    print(f"Configuring {plugin_name} in {rc_path}...")

    # Add comment line (with blank line before it)
    updated_content = add_line_to_config(
        rc_path,
        comment_line,
        add_blank_line_before=True,
    )
    rc_path.write_text(updated_content)

    # Add configuration line based on mode
    if fpath_mode:
        # For completion plugins, add to fpath
        config_line = f"fpath=(~/.zsh/{plugin_name}/src $fpath)"
    else:
        # For regular plugins, source the main file
        config_line = f"source ~/.zsh/{plugin_name}/{source_file}"

    updated_content = add_line_to_config(
        rc_path,
        config_line,
        add_blank_line_before=False,
    )
    rc_path.write_text(updated_content)

    print(f"{plugin_name} configuration added to {rc_path}")

    if was_cloned:
        print(f"Please restart your shell or run: source {rc_path}")

    return was_cloned
