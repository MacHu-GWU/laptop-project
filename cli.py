# -*- coding: utf-8 -*-

import fire

from laptop.tools.pyenv import install_pyenv
from laptop.tools.oh_my_zsh import install_oh_my_zsh


class Command:
    def install_pyenv(self):
        install_pyenv()

    def install_oh_my_zsh(self):
        install_oh_my_zsh()


fire.Fire(Command())
