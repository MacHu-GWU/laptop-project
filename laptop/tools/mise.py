# -*- coding: utf-8 -*-

"""
mise-en-place Installation and Configuration

This module handles the installation of mise (formerly rtx), a polyglot runtime manager
that replaces tools like asdf, pyenv, nvm, rbenv, etc.

Official documentation: https://mise.jdx.dev/
"""

import subprocess

from ..utils import is_command_installed
from ..utils import add_line_to_config
from ..vendor.which_shell import shell


def is_mise_installed() -> bool:
    """
    Check if mise is installed and available in PATH.

    Returns:
        True if mise is installed, False otherwise
    """
    return is_command_installed("mise")


def _install_mise() -> None:
    """
    Download and install mise using the official installation script.

    This function downloads the mise installation script from https://mise.run
    and executes it via sh. It does not check if mise is already installed -
    that check should be done by the caller.

    Raises:
        subprocess.CalledProcessError: If the installation script fails
    """
    print("Installing mise-en-place...")

    # Download the installation script
    curl_process = subprocess.Popen(
        ["curl", "-fsSL", "https://mise.run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Pipe the downloaded script to sh
    install_result = subprocess.run(
        ["sh"],
        stdin=curl_process.stdout,
        capture_output=True,
        text=True,
    )

    # Wait for curl to complete and check for errors
    curl_process.stdout.close()
    curl_process.wait()

    if install_result.returncode != 0:
        raise subprocess.CalledProcessError(
            install_result.returncode,
            ["sh"],
            output=install_result.stdout,
            stderr=install_result.stderr,
        )

    print("mise installation completed successfully!")


def install_mise() -> bool:
    """
    Install mise-en-place and configure shell integration.

    See: https://mise.jdx.dev/

    This function:
    1. Checks if mise is already installed (idempotent)
    2. Downloads and installs mise using the official install script
    3. Adds the mise activation line to the appropriate shell RC file

    The function is idempotent - it's safe to run multiple times.

    Returns:
        True if installation was performed, False if mise was already installed

    Raises:
        subprocess.CalledProcessError: If the installation script fails
        NotImplementedError: If the current shell is not supported

    Example:
        >>> install_mise()
        True  # mise was installed
        >>> install_mise()
        False  # mise was already installed (idempotent)
    """
    # Check if mise is already installed
    if is_mise_installed():
        print("mise is already installed, skipping installation...")
        # Still ensure the activation line is in the RC file
        _add_mise_activation_to_rc()
        return False

    # Download and install mise
    _install_mise()

    # Add mise activation to shell RC file
    _add_mise_activation_to_rc()

    return True


def _add_mise_activation_to_rc() -> None:
    """
    Add mise activation line to the appropriate shell RC file.

    This function:
    1. Detects the current shell (zsh, bash, or sh)
    2. Determines the appropriate mise activation command
    3. Adds the activation line to the RC file (idempotent)

    The activation line will be:
        - For zsh:  eval "$(mise activate zsh)"
        - For bash: eval "$(mise activate bash)"
        - For sh:   eval "$(mise activate sh)"

    Raises:
        NotImplementedError: If the current shell is not supported
    """
    rc_path = shell.rc_path

    # Determine the activation command based on shell type
    if shell.is_zsh:
        activation_line = 'eval "$(mise activate zsh)"'
    elif shell.is_bash:
        activation_line = 'eval "$(mise activate bash)"'
    elif shell.is_sh:
        activation_line = 'eval "$(mise activate sh)"'
    else:
        raise NotImplementedError(f"Unsupported shell: {shell.shell_name}")

    # Add a descriptive comment and the activation line
    comment_line = "# Enable mise - polyglot runtime manager"

    print(f"Adding mise activation to {rc_path}...")

    # Add comment line (with blank line before it)
    updated_content = add_line_to_config(
        rc_path,
        comment_line,
        add_blank_line_before=True,
    )
    rc_path.write_text(updated_content)

    # Add activation line (without blank line before it, since comment is right above)
    updated_content = add_line_to_config(
        rc_path,
        activation_line,
        add_blank_line_before=False,
    )
    rc_path.write_text(updated_content)

    print(f"mise activation added to {rc_path}")
    print(f"Please restart your shell or run: source {rc_path}")
