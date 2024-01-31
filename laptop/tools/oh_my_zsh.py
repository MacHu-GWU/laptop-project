# -*- coding: utf-8 -*-

import subprocess
import urllib.request

from ..paths import dir_home
from ..utils import add_line
from ..vendor.shell import path_rc

from ..paths import dir_github


dir_oh_my_zsh = dir_home.joinpath(".oh-my-zsh")


def is_oh_my_zsh_installed() -> bool:
    return dir_oh_my_zsh.exists()


def install_oh_my_zsh():
    url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8").strip()
    if is_oh_my_zsh_installed() is False:
        subprocess.run(["sh", "-c", content])


# ------------------------------------------------------------------------------
# Install zsh plugins
# ------------------------------------------------------------------------------
def install_zsh_syntax_highlighting():
    print("try to install zsh-syntax-highlighting plugin ...")
    dir_repo_zsh_syntax_highlighting = dir_github / "zsh-syntax-highlighting"
    if not dir_repo_zsh_syntax_highlighting.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/zsh-users/zsh-syntax-highlighting.git",
                f"{dir_repo_zsh_syntax_highlighting}",
            ],
            check=True,
        )
    else:
        print("  already installed")


def install_zsh_autocomplete():
    print("try to install zsh-autocomplete plugin ...")
    dir_repo_zsh_autocomplete = dir_github / "zsh-autocomplete"
    if not dir_repo_zsh_autocomplete.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/marlonrichert/zsh-autocomplete.git",
                f"{dir_repo_zsh_autocomplete}",
            ],
            check=True,
        )
    else:
        print("  already installed")


def install_zsh_autosuggestions():
    print("try to install zsh-autosuggestions plugin ...")
    dir_repo_zsh_autosuggestions = dir_github / "zsh-autosuggestions"
    if not dir_repo_zsh_autosuggestions.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/zsh-users/zsh-autosuggestions.git",
                f"{dir_repo_zsh_autosuggestions}",
            ],
            check=True,
        )
    else:
        print("  already installed")


def install_zsh_powerlevel10k():
    print("try to install powerlevel10k theme ...")
    dir_repo_zsh_powerlevel10k = dir_oh_my_zsh / "custom" / "themes" / "powerlevel10k"
    if not dir_repo_zsh_powerlevel10k.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/romkatv/powerlevel10k.git",
                f"{dir_repo_zsh_powerlevel10k}",
            ],
            check=True,
        )
    else:
        print("  already installed")
    add_line(
        path_rc,
        [
            'export LANG="en_US.UTF-8"',
            'export LC_ALL="en_US.UTF-8"',
        ],
    )
