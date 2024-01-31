# -*- coding: utf-8 -*-

import subprocess
import urllib.request

from ..paths import dir_home
from ..utils import add_line
from ..vendor.shell import path_rc


dir_oh_my_zsh = dir_home.joinpath(".oh-my-zsh")


def is_oh_my_zsh_installed() -> bool:
    return dir_oh_my_zsh.exists()


def install_oh_my_zsh():
    url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8").strip()
    if is_oh_my_zsh_installed() is False:
        subprocess.run(["sh", "-c", content])
