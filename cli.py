# -*- coding: utf-8 -*-

import fire

from laptop.tools.pyenv import install_pyenv


class Command:
    def install_pyenv(self):
        install_pyenv()


fire.Fire(Command())
