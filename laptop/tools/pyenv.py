# -*- coding: utf-8 -*-

import subprocess

from ..paths import dir_home
from ..utils import add_line
from ..vendor.os_platform import IS_LINUX, IS_MACOS
from ..vendor.shell import IS_ZSH, IS_BASH, IS_SH, path_rc


dir_pyenv = dir_home.joinpath(".pyenv")


def is_pyenv_installed() -> bool:
    return dir_pyenv.exists()


def install_pyenv():
    if is_pyenv_installed() is False:
        pipe = subprocess.Popen(["curl", "https://pyenv.run"], stdout=subprocess.PIPE)
        subprocess.run(["bash"], stdin=pipe.stdout)
    add_line(
        path_rc,
        [
            "#------------------------------------------------------------",
            "# Enable pyenv - Python environment manager",
            'export PYENV_ROOT="$HOME/.pyenv"',
            'export PATH="$PYENV_ROOT/bin:$PATH"',
            'eval "$(pyenv init --path)"',
        ],
    )
