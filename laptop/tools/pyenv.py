# -*- coding: utf-8 -*-

import subprocess

from ..paths import dir_home
from ..vendor.os_platform import IS_LINUX, IS_MACOS


dir_pyenv = dir_home.joinpath(".pyenv")


def is_pyenv_installed() -> bool:
    return dir_pyenv.exists()


def install_pyenv():
    if is_pyenv_installed() is False:
        pipe = subprocess.Popen(["curl", "https://pyenv.run"], stdout=subprocess.PIPE)
        subprocess.run(["bash"], stdin=pipe.stdout)
