# -*- coding: utf-8 -*-

from laptop import api


def test():
    _ = api


if __name__ == "__main__":
    from laptop.tests import run_cov_test

    run_cov_test(__file__, "laptop.api", preview=False)
