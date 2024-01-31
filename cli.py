# -*- coding: utf-8 -*-

import fire

from laptop.tools.pyenv import install_pyenv
from laptop.tools.oh_my_zsh import (
    install_oh_my_zsh,
    install_zsh_syntax_highlighting,
    install_zsh_autocomplete,
    install_zsh_autosuggestions,
    install_zsh_powerlevel10k,
)


class Command:
    def install_pyenv(self):
        install_pyenv()

    def install_oh_my_zsh(self):
        install_oh_my_zsh()

    def install_zsh_syntax_highlighting(self):
        install_zsh_syntax_highlighting()

    def install_zsh_autocomplete(self):
        install_zsh_autocomplete()

    def install_zsh_autosuggestions(self):
        install_zsh_autosuggestions()

    def install_zsh_powerlevel10k(self):
        install_zsh_powerlevel10k()


fire.Fire(Command())
