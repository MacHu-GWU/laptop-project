# -*- coding: utf-8 -*-

import shutil

from laptop.paths import path_enum
from laptop.utils import add_line_to_config
from laptop.utils import is_command_installed
from laptop.utils import git_clone


def test_add_line_to_config():
    """Test add_line_to_config function with various scenarios."""
    tmp_dir = path_enum.dir_project_root / "tests" / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    test_file = tmp_dir / "test_config_temp.txt"

    # Test 1: Add line to empty file with blank line before (default)
    test_file.write_text("")
    result = add_line_to_config(
        test_file,
        "export PATH=$PATH:/new/path",
        add_blank_line_before=True,
    )
    assert result == "\n\nexport PATH=$PATH:/new/path\n"

    # Test 2: Add line to file with existing content with blank line before
    test_file.write_text("# Config file\nalias ll='ls -la'\n")
    result = add_line_to_config(
        test_file,
        "export EDITOR=vim",
        add_blank_line_before=True,
    )
    assert result == "# Config file\nalias ll='ls -la'\n\nexport EDITOR=vim\n"

    # Test 3: Add line without blank line before
    test_file.write_text("# Config file\nalias ll='ls -la'\n")
    result = add_line_to_config(
        test_file,
        "export EDITOR=vim",
        add_blank_line_before=False,
    )
    assert result == "# Config file\nalias ll='ls -la'\nexport EDITOR=vim\n"

    # Test 4: Idempotency - line already exists (should not modify)
    test_file.write_text("# Config file\nexport EDITOR=vim\nalias ll='ls -la'\n")
    result = add_line_to_config(
        test_file,
        "export EDITOR=vim",
        add_blank_line_before=True,
    )
    assert result == "# Config file\nexport EDITOR=vim\nalias ll='ls -la'\n"

    # Test 5: File without trailing newline - line doesn't exist
    test_file.write_text("# Config file")
    result = add_line_to_config(
        test_file, "export LANG=en_US.UTF-8", add_blank_line_before=True
    )
    assert result == "# Config file\n\nexport LANG=en_US.UTF-8\n"

    # Test 6: File without trailing newline - line already exists
    test_file.write_text("# Config file\nexport LANG=en_US.UTF-8")
    result = add_line_to_config(
        test_file,
        "export LANG=en_US.UTF-8",
        add_blank_line_before=True,
    )
    assert result == "# Config file\nexport LANG=en_US.UTF-8\n"

    # Test 7: Multiple trailing newlines should be normalized
    test_file.write_text("# Config file\n\n\n")
    result = add_line_to_config(
        test_file,
        "source ~/.zsh_aliases",
        add_blank_line_before=True,
    )
    assert result == "# Config file\n\nsource ~/.zsh_aliases\n"

    # Test 8: Line exists as substring but not as exact line (should still add)
    test_file.write_text("# This is a comment about PATH\n")
    result = add_line_to_config(test_file, "PATH", add_blank_line_before=True)
    # "PATH" is a substring in the comment, but not an exact line, so it should be added
    assert result == "# This is a comment about PATH\n\nPATH\n"

    # Test 9: Exact line match (should not add duplicate)
    test_file.write_text("export PATH=$PATH:/usr/local/bin\n# Another line\n")
    result = add_line_to_config(
        test_file,
        "export PATH=$PATH:/usr/local/bin",
        add_blank_line_before=True,
    )
    # Line already exists as exact match, should not be modified
    assert result == "export PATH=$PATH:/usr/local/bin\n# Another line\n"

    # Clean up
    if test_file.exists():
        test_file.unlink()


def test_is_command_installed():
    """Test is_command_installed function with common and rare commands."""
    # Test 1: Check a command that definitely exists (python)
    assert is_command_installed("python") or is_command_installed("python3"), \
        "Python should be installed in the test environment"

    # Test 2: Check another common command (ls on Unix-like systems)
    assert is_command_installed("ls"), \
        "ls command should be available on Unix-like systems"

    # Test 3: Check a command that likely doesn't exist
    # ansible-playbook is a useful tool but not commonly installed by default
    rare_commands = [
        "ansible-playbook",  # Ansible automation tool
        "terraform",         # Infrastructure as code tool
        "packer",           # Image building tool
        "kubectl",          # Kubernetes CLI
        "helm",             # Kubernetes package manager
    ]

    # At least one of these should not be installed in a typical environment
    # We're testing that the function correctly returns False for non-existent commands
    all_rare_installed = all(is_command_installed(cmd) for cmd in rare_commands)
    assert not all_rare_installed, \
        "At least one rare command should not be installed (for testing purposes)"

    # Test 4: Check a definitely non-existent command
    assert not is_command_installed("this-command-definitely-does-not-exist-xyz123"), \
        "Non-existent command should return False"

    # Test 5: Empty string should return False
    assert not is_command_installed(""), \
        "Empty string should return False"


def test_git_clone():
    """Test git_clone function with various scenarios."""
    test_repo_url = "https://github.com/zsh-users/zsh-syntax-highlighting"
    tmp_dir = path_enum.dir_project_root / "tests" / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    test_dir = tmp_dir / "test_git_repo"

    # Clean up before tests
    if test_dir.exists():
        shutil.rmtree(test_dir)

    try:
        # Test 1: Basic clone with default depth
        result = git_clone(test_repo_url, test_dir)
        assert result is True, "Should return True when cloning is performed"
        assert test_dir.exists(), "Repository directory should exist"
        assert (test_dir / ".git").exists(), ".git directory should exist"

        # Test 2: Idempotent - clone again with force_reclone=False (should skip)
        result = git_clone(test_repo_url, test_dir, force_reclone=False)
        assert result is False, "Should return False when skipping (idempotent)"
        assert test_dir.exists(), "Repository directory should still exist"

        # Test 3: Force re-clone with force_reclone=True
        result = git_clone(test_repo_url, test_dir, force_reclone=True)
        assert result is True, "Should return True when re-cloning"
        assert test_dir.exists(), "Repository directory should exist after re-clone"
        assert (test_dir / ".git").exists(), ".git directory should exist after re-clone"

        # Clean up for next test
        shutil.rmtree(test_dir)

        # Test 4: Clone with specific branch
        result = git_clone(test_repo_url, test_dir, branch="master")
        assert result is True, "Should successfully clone with branch"
        assert test_dir.exists(), "Repository directory should exist"

        # Clean up for next test
        shutil.rmtree(test_dir)

        # Test 5: Clone with specific depth
        result = git_clone(test_repo_url, test_dir, depth=5)
        assert result is True, "Should successfully clone with custom depth"
        assert test_dir.exists(), "Repository directory should exist"

        # Clean up for next test
        shutil.rmtree(test_dir)

        # Test 6: Clone with specific tag
        # Note: This test might fail if the tag doesn't exist, but we're testing the functionality
        result = git_clone(test_repo_url, test_dir, tag="0.8.0", depth=1)
        assert result is True, "Should successfully clone with tag"
        assert test_dir.exists(), "Repository directory should exist"

        # Test 7: Error when both branch and tag are specified
        shutil.rmtree(test_dir)
        try:
            git_clone(test_repo_url, test_dir, branch="master", tag="v1.0.0")
            assert False, "Should raise ValueError when both branch and tag are specified"
        except ValueError as e:
            assert "Cannot specify both branch and tag" in str(e)

        # Test 8: Error when destination exists but is not a git repo
        test_dir.mkdir(parents=True)
        (test_dir / "somefile.txt").write_text("not a git repo")
        try:
            git_clone(test_repo_url, test_dir)
            assert False, "Should raise ValueError when destination exists without .git"
        except ValueError as e:
            assert "does not contain a .git directory" in str(e)

    finally:
        # Final cleanup
        if test_dir.exists():
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    from laptop.tests import run_cov_test

    run_cov_test(
        __file__,
        "laptop.utils",
        preview=False,
    )
