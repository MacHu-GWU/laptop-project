# -*- coding: utf-8 -*-

import os

from .pathlib_mate import Path


IS_SH = False
IS_BASH = False
IS_ZSH = False

if os.environ["SHELL"] == "/bin/zsh":
    IS_ZSH = True
    path_rc = Path.home().joinpath(".zshrc")
elif os.environ["SHELL"] == "/bin/bash":
    IS_BASH = True
    path_rc = Path.home().joinpath(".bashrc")
elif os.environ["SHELL"] == "/bin/sh":
    IS_SH = True
    path_rc = Path.home().joinpath(".shrc")
else:
    raise NotImplementedError
