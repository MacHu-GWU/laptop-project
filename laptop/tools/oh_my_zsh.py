# -*- coding: utf-8 -*-

import subprocess
import urllib.request

from ..paths import dir_home, dir_github, dir_home_stuff
from ..vendor.os_platform import IS_LINUX, IS_MACOS


dir_oh_my_zsh = dir_home.joinpath(".oh-my-zsh")
path_zshrc = dir_home.joinpath(".zshrc")

path_p10k_zsh = dir_home_stuff / ".p10k.zsh"

if IS_MACOS:
    path_p10k_zsh_source = dir_home_stuff / ".p10k.zsh-for-MacOS"
elif IS_LINUX:
    path_p10k_zsh_source = dir_home_stuff / ".p10k.zsh-for-Linux"
else:
    raise NotImplementedError

path_zshrc_source = dir_home_stuff / ".zshrc"


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


def install_all_zsh_plugins():
    install_zsh_syntax_highlighting()
    install_zsh_autocomplete()
    install_zsh_autosuggestions()
    install_zsh_powerlevel10k()


def copy_zsh_config():
    print("copy zsh config ...")
    path_p10k_zsh.write_text(path_p10k_zsh_source.read_text())
    path_zshrc.write_text(
        path_zshrc_source.read_text().replace("{{ dir_github }}", str(dir_github))
    )
