# -*- coding: utf-8 -*-

"""
Starship.rs Installation and Configuration

This module handles the installation of Starship, a cross-platform shell prompt
written in Rust. Starship is minimal, fast, and highly customizable.

Official documentation: https://starship.rs/
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..utils import is_command_installed
from ..utils import add_line_to_config
from ..vendor.which_shell import shell


def is_starship_installed() -> bool:
    """
    Check if starship is installed and available in PATH.

    Returns:
        True if starship is installed, False otherwise
    """
    return is_command_installed("starship")


def _install_starship() -> None:
    """
    Download and install starship using the official installation script.

    This function downloads the starship installation script from starship.rs
    and executes it via sh. It does not check if starship is already installed -
    that check should be done by the caller.

    Raises:
        subprocess.CalledProcessError: If the installation script fails
    """
    print("Installing starship.rs...")

    # Download the installation script
    curl_process = subprocess.Popen(
        ["curl", "-sS", "https://starship.rs/install.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Pipe the downloaded script to sh with -s flag for non-interactive install
    install_result = subprocess.run(
        ["sh", "-s", "--", "-y"],  # -y flag for auto-confirm
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

    print("starship installation completed successfully!")


def _configure_starship_preset() -> None:
    """
    Configure starship with the no-nerd-font preset.

    This function:
    1. Creates ~/.config directory if it doesn't exist
    2. Runs 'starship preset no-nerd-font -o ~/.config/starship.toml'
       to generate the configuration file

    The no-nerd-font preset is suitable for terminals without Nerd Font support.

    Raises:
        subprocess.CalledProcessError: If the preset command fails
    """
    print("Configuring starship preset (no-nerd-font)...")

    # Ensure ~/.config directory exists
    config_dir = Path.home() / ".config"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Configure starship with no-nerd-font preset
    starship_config_path = config_dir / "starship.toml"

    result = subprocess.run(
        ["starship", "preset", "no-nerd-font", "-o", str(starship_config_path)],
        capture_output=True,
        text=True,
        check=True,
    )

    print(f"starship configuration written to {starship_config_path}")


def _add_starship_activation_to_rc() -> None:
    """
    Add starship activation line to the appropriate shell RC file.

    This function:
    1. Detects the current shell (zsh, bash, or sh)
    2. Determines the appropriate starship init command
    3. Adds the activation line to the RC file (idempotent)

    The activation line will be:
        - For zsh:  eval "$(starship init zsh)"
        - For bash: eval "$(starship init bash)"
        - For sh:   eval "$(starship init sh)"

    Raises:
        NotImplementedError: If the current shell is not supported
    """
    rc_path = shell.rc_path

    # Determine the activation command based on shell type
    if shell.is_zsh:
        activation_line = 'eval "$(starship init zsh)"'
    elif shell.is_bash:
        activation_line = 'eval "$(starship init bash)"'
    elif shell.is_sh:
        activation_line = 'eval "$(starship init sh)"'
    else:
        raise NotImplementedError(f"Unsupported shell: {shell.shell_name}")

    # Add a descriptive comment and the activation line
    comment_line = "# Enable starship - cross-platform shell prompt"

    print(f"Adding starship activation to {rc_path}...")

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

    print(f"starship activation added to {rc_path}")
    print(f"Please restart your shell or run: source {rc_path}")


def install_starship() -> bool:
    """
    Install starship.rs and configure shell integration.

    This function:
    1. Checks if starship is already installed (idempotent)
    2. Downloads and installs starship using the official install script
    3. Configures starship with the no-nerd-font preset
    4. Adds the starship activation line to the appropriate shell RC file

    The function is idempotent - it's safe to run multiple times.

    Returns:
        True if installation was performed, False if starship was already installed

    Raises:
        subprocess.CalledProcessError: If the installation script fails
        NotImplementedError: If the current shell is not supported

    Example:
        >>> install_starship()
        True  # starship was installed
        >>> install_starship()
        False  # starship was already installed (idempotent)
    """
    # Check if starship is already installed
    if is_starship_installed():
        print("starship is already installed, skipping installation...")
        # Still ensure the activation line is in the RC file
        _add_starship_activation_to_rc()
        # Still ensure the preset is configured
        _configure_starship_preset()
        return False

    # Download and install starship
    _install_starship()

    # Configure starship preset
    _configure_starship_preset()

    # Add starship activation to shell RC file
    _add_starship_activation_to_rc()

    return True
