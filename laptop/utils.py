# -*- coding: utf-8 -*-

import typing as T

from pathlib import Path


def add_line_to_config(
    path: Path,
    line: str,
    add_blank_line_before: bool = True,
) -> str:
    """
    Add a line to a configuration file (e.g., .zshrc) in an idempotent way.

    This function reads the file content, checks if the line already exists,
    and only modifies the content if the line is not present. It ensures the
    file ends with a newline character.

    Args:
        path: Path to the configuration file
        line: The line to add (without trailing newline)
        add_blank_line_before: If True, add a blank line before the new line (default: True)

    Returns:
        The modified file content as a string (with trailing newline)

    Examples:
        >>> content = add_line_to_config(Path(".zshrc"), "export PATH=$PATH:/usr/local/bin")
        >>> # If line doesn't exist, adds it with a blank line before it

        >>> content = add_line_to_config(Path(".zshrc"), "alias ll='ls -la'", add_blank_line_before=False)
        >>> # Adds the line without a blank line before it
    """
    # Read the existing content
    content = path.read_text()

    # Split content into lines for exact line matching
    lines = content.splitlines()

    # Check if the line already exists (exact match)
    if line in lines:
        # Line already exists, return original content
        # Ensure it ends with newline
        if not content.endswith("\n"):
            return content + "\n"
        return content

    # Line doesn't exist, we need to add it
    # Remove trailing newline(s) to normalize
    content = content.rstrip("\n")

    # Build the new content
    if add_blank_line_before:
        # Add blank line before the new line
        new_content = content + "\n\n" + line + "\n"
    else:
        # Add the line directly
        new_content = content + "\n" + line + "\n"

    return new_content
