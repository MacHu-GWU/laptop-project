# -*- coding: utf-8 -*-

from .vendor.pathlib_mate import Path
from .vendor.os_platform import IS_MACOS
from .vendor.runtime import runtime

dir_python_lib = Path(__file__).absolute().parent
PACKAGE_NAME = dir_python_lib.name

dir_project_root = dir_python_lib.parent
dir_home_stuff = dir_project_root.joinpath("home-stuff")

dir_home = Path.home()

if runtime.is_aws_cloud9:
    dir_github = dir_home.joinpath("environment", "GitHub")
elif IS_MACOS:
    dir_github = dir_home.joinpath("Document", "GitHub")
else:
    raise NotImplementedError

dir_github.mkdir_if_not_exists()

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"
