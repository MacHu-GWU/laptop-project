#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Laptop Development Environment Bootstrap CLI

A zero-dependency CLI tool for setting up development environments.
Uses only Python standard library (argparse) for command-line interface.

Usage:
    python cli.py install mise       # Install mise-en-place
    python cli.py --help             # Show help message
    python cli.py install --help     # Show install subcommands
"""

import argparse
import sys

from laptop.tools.mise import install_mise


# ==============================================================================
# Old Commands (Deprecated - using fire library)
# ==============================================================================
# import fire
#
# from laptop.tools.pyenv import install_pyenv
# from laptop.tools.oh_my_zsh import (
#     install_oh_my_zsh,
#     install_zsh_syntax_highlighting,
#     install_zsh_autocomplete,
#     install_zsh_autosuggestions,
#     install_zsh_powerlevel10k,
#     install_all_zsh_plugins,
#     copy_zsh_config,
# )
#
#
# class Command:
#     def install_pyenv(self):
#         install_pyenv()
#
#     def install_oh_my_zsh(self):
#         install_oh_my_zsh()
#
#     def install_zsh_syntax_highlighting(self):
#         install_zsh_syntax_highlighting()
#
#     def install_zsh_autocomplete(self):
#         install_zsh_autocomplete()
#
#     def install_zsh_autosuggestions(self):
#         install_zsh_autosuggestions()
#
#     def install_zsh_powerlevel10k(self):
#         install_zsh_powerlevel10k()
#
#     def install_all_zsh_plugins(self):
#         install_all_zsh_plugins()
#
#     def copy_zsh_config(self):
#         copy_zsh_config()
#
#
# fire.Fire(Command())
# ==============================================================================


def make_install_command(
    install_func,
    success_message: str = "Installation completed successfully!",
    already_installed_message: str = "Already installed and configured",
    error_message_prefix: str = "Error during installation",
):
    """
    Factory function to create installation command handlers.

    This function returns a command handler that can be used with argparse.
    It standardizes the installation workflow: execute install function,
    handle return value (True for new install, False for skip), and
    provide consistent error handling.

    Args:
        install_func: The installation function to call (should return bool)
        success_message: Message to display when installation succeeds (new install)
        already_installed_message: Message to display when already installed (idempotent)
        error_message_prefix: Prefix for error messages

    Returns:
        A command handler function suitable for argparse

    Example:
        >>> cmd_install_mise = make_install_command(
        ...     install_mise,
        ...     success_message="mise installation completed successfully!",
        ...     already_installed_message="mise is already installed and configured",
        ...     error_message_prefix="Error installing mise",
        ... )
    """

    def command_handler(args):
        """Generated command handler."""
        try:
            result = install_func()
            if result:
                print(f"\n✓ {success_message}")
                sys.exit(0)
            else:
                print(f"\n✓ {already_installed_message}")
                sys.exit(0)
        except Exception as e:
            print(f"\n✗ {error_message_prefix}: {e}", file=sys.stderr)
            sys.exit(1)

    return command_handler


def setup_install_subcommands(subparsers):
    """Set up the 'install' subcommand group."""
    install_parser = subparsers.add_parser(
        "install",
        help="Install development tools",
        description="Install various development tools and configure them",
    )

    # Create subparsers for install commands
    install_subparsers = install_parser.add_subparsers(
        dest="tool",
        help="Tool to install",
        required=True,
    )

    # install mise
    mise_parser = install_subparsers.add_parser(
        "mise",
        help="Install mise-en-place (polyglot runtime manager)",
        description="Install mise-en-place and configure shell integration. "
        "mise is a modern replacement for asdf, pyenv, nvm, rbenv, etc.",
    )
    # Create command handler using factory function
    cmd_install_mise = make_install_command(
        install_func=install_mise,
        success_message="mise installation completed successfully!",
        already_installed_message="mise is already installed and configured",
        error_message_prefix="Error installing mise",
    )
    mise_parser.set_defaults(func=cmd_install_mise)

    # Example: How to add more tools
    # --------------------------------
    # # install starship
    # starship_parser = install_subparsers.add_parser(
    #     "starship",
    #     help="Install starship.rs (cross-platform shell prompt)",
    #     description="Install starship and configure shell integration.",
    # )
    # cmd_install_starship = make_install_command(
    #     install_func=install_starship,  # from laptop.tools.starship import install_starship
    #     success_message="starship installation completed successfully!",
    #     already_installed_message="starship is already installed and configured",
    #     error_message_prefix="Error installing starship",
    # )
    # starship_parser.set_defaults(func=cmd_install_starship)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="laptop",
        description="Laptop Development Environment Bootstrap Tool",
        epilog="For more information, visit: https://github.com/your-repo/laptop-project",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.1",
    )

    # Create subparsers for main commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=True,
    )

    # Set up install subcommands
    setup_install_subcommands(subparsers)

    # Parse arguments
    args = parser.parse_args()

    # Execute the command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
