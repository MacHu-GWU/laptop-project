# -*- coding: utf-8 -*-

from laptop.paths import dir_unit_test
from laptop.utils import add_line


def test_add_line():
    p = dir_unit_test.joinpath("test_add_line.txt")
    p.write_text("hello\nworld\n")
    add_line(p, "hello")
    add_line(p, "alice")

    assert p.read_text().split("\n") == ["hello", "world", "", "alice", ""]


if __name__ == "__main__":
    from laptop.tests import run_cov_test

    run_cov_test(__file__, "laptop.utils", preview=False)
