# -*- coding: utf-8 -*-

from __future__ import annotations

import shutil
import subprocess

from pathlib import Path


def add_line_to_config(
    path: Path,
    line: str,
    add_blank_line_before: bool = True,
) -> str:
    """
    Add a line to a configuration file (e.g., .zshrc) in an idempotent way.

    This function reads the file content (or treats non-existent files as empty),
    checks if the line already exists, and only modifies the content if the line
    is not present. It ensures the file ends with a newline character.

    Args:
        path: Path to the configuration file (file may or may not exist)
        line: The line to add (without trailing newline)
        add_blank_line_before: If True, add a blank line before the new line (default: True)

    Returns:
        The modified file content as a string (with trailing newline)

    Examples:
        >>> content = add_line_to_config(Path(".zshrc"), "export PATH=$PATH:/usr/local/bin")
        >>> # If line doesn't exist, adds it with a blank line before it

        >>> content = add_line_to_config(Path(".zshrc"), "alias ll='ls -la'", add_blank_line_before=False)
        >>> # Adds the line without a blank line before it

        >>> content = add_line_to_config(Path("new_config.txt"), "first line")
        >>> # Works even if new_config.txt doesn't exist (treats as empty file)
    """
    # Read the existing content, treat non-existent file as empty string
    if path.exists():
        content = path.read_text()
    else:
        content = ""

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


def is_command_installed(command: str) -> bool:
    """
    Check if a command-line tool is installed and available in PATH.

    This function uses shutil.which to check if a command can be found
    in the system's PATH environment variable.

    Args:
        command: The name of the command to check (e.g., 'git', 'python', 'mise')

    Returns:
        True if the command is installed and found in PATH, False otherwise

    Examples:
        >>> is_command_installed('python')
        True
        >>> is_command_installed('some-nonexistent-command-xyz')
        False
    """
    return shutil.which(command) is not None


def git_clone(
    url: str,
    path: Path,
    depth: int | None = 1,
    branch: str | None = None,
    tag: str | None = None,
    force_reclone: bool = False,
) -> bool:
    """
    Clone a git repository to the specified path with idempotent behavior.

    Args:
        url: Git repository URL (e.g., 'https://github.com/user/repo.git')
        path: Destination path where the repository will be cloned
        depth: Clone depth for shallow clone (default: 1). Set to None for full clone.
        branch: Branch name to clone (mutually exclusive with tag)
        tag: Tag name to clone (mutually exclusive with branch)
        force_reclone: If True, delete and re-clone if destination exists with .git dir.
                       If False, skip cloning if destination already exists (idempotent).

    Returns:
        True if cloning was performed, False if skipped (when force_reclone=False
        and destination already exists)

    Raises:
        ValueError: If both branch and tag are specified, or if destination exists
                    without a .git directory
        subprocess.CalledProcessError: If git clone command fails

    Examples:
        >>> # Clone a repository with default shallow clone (depth=1)
        >>> git_clone("https://github.com/user/repo.git", Path("/tmp/repo"))

        >>> # Clone a specific branch
        >>> git_clone("https://github.com/user/repo.git", Path("/tmp/repo"), branch="main")

        >>> # Clone a specific tag with full history
        >>> git_clone("https://github.com/user/repo.git", Path("/tmp/repo"), depth=None, tag="v1.0.0")

        >>> # Force re-clone if destination exists
        >>> git_clone("https://github.com/user/repo.git", Path("/tmp/repo"), force_reclone=True)
    """
    # Validate that branch and tag are mutually exclusive
    if branch is not None and tag is not None:
        raise ValueError("Cannot specify both branch and tag")

    # Check if destination exists
    if path.exists():
        git_dir = path / ".git"

        if git_dir.exists():
            # Destination is a git repository
            if force_reclone:
                # Delete and re-clone
                shutil.rmtree(path)
            else:
                # Skip cloning (idempotent behavior)
                return False
        else:
            # Destination exists but is not a git repository
            raise ValueError(
                f"Destination path {path} exists but does not contain a .git directory. "
                f"Cannot clone repository here."
            )

    # Build git clone command
    cmd = ["git", "clone"]

    # Add depth argument for shallow clone
    if depth is not None:
        cmd.extend(["--depth", str(depth)])

    # Add branch or tag
    if branch is not None:
        cmd.extend(["--branch", branch])
    elif tag is not None:
        cmd.extend(["--branch", tag])

    # Add URL and destination path
    cmd.extend([url, str(path)])

    # Execute git clone
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    return True
