# -*- coding: utf-8 -*-

from laptop.vendor.fire import Fire
from laptop.tools.pyenv import install_pyenv


class Command:
    def install_pyenv(self):
        install_pyenv()


Fire(Command())
