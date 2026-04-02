# -*- coding: utf-8 -*-

from laptop.paths import path_enum
from laptop.utils import add_line_to_config


def test_add_line_to_config():
    """Test add_line_to_config function with various scenarios."""
    test_file = path_enum.dir_project_root / "tests" / "data" / "test_config_temp.txt"

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


if __name__ == "__main__":
    from laptop.tests import run_cov_test

    run_cov_test(
        __file__,
        "laptop.utils",
        preview=False,
    )
