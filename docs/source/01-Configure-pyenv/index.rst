Configure pyenv
==============================================================================
注: 本文的所有内容均有自动化脚本实现自动安装, 请前往 :ref:`configure-pyenv-automatically` 查看.


Overview
------------------------------------------------------------------------------
在同一台电脑上同时拥有多个 Python 版本是专业 Python 开发者的刚需. Homebrew 里的 Python 发行版的选择余地非常小, 建议不要用 Homebrew 来管理 Python.

社区里最主流的工具是 ``pyenv``, 它类似于 ``rbenv`` (ruby env), 能通过用一个 shim (插销) 修改你的 ``$PATH``, 使得你打 ``python`` 这个命令时会先到 ``pyenv`` 的 shell script 中去找, 这个 shell script 里实现了具体的寻找真正的 Python 解释器的逻辑.

``pyenv`` 这个工具不需要 sudo, 所有的安装都在 ``${HOME}/.pyenv`` 下. 删除掉这个目录就什么都删除了, 非常干净.


Install Pyenv
------------------------------------------------------------------------------
官方文档 `Install pyenv <https://github.com/pyenv/pyenv?tab=readme-ov-file#installation>`_ 中有一个脚本可以一键安装. 它本质是把一个 shell script 脚本保存到了 ``https://pyenv.run``, 然后用 bash 执行. 这个方法跟 homebrew 一样, 非常 hacky.

.. code-block:: bash

    curl https://pyenv.run | bash

安装好之后你要给你的 ``.zshrc`` (或 ``.bashrc``, 取决于你用哪个 shell) 中添加如下内容. 这些内容的本质是修改 Path, 启动 SHIM 插销机制.

.. code-block:: bash

    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"


Important Commands
------------------------------------------------------------------------------
- List all available version: ``pyenv install -l``.
- Install specified version: ``pyenv install <version>``.
- Made multiple python versions available in global / local / shell: ``pyenv global <version1> <version2> ...``, ``pyenv local <version1> <version2> ...``, ``pyenv shell <version1> <version2> ...``.
- Check current version: ``pyenv version``.
- Check all installed version: ``pyenv versions``.


Install Build Dependencies
------------------------------------------------------------------------------
使用 Pyenv 安装 Python 的本质是从 Python 的 C 源码构建. 构建 C 源码是需要一些编译器等依赖工具的. `Suggested build environment <https://github.com/pyenv/pyenv/wiki#suggested-build-environment>`_ 这篇文档介绍了在不同的操作系统上 build Python 所需的依赖. 你需要手动执行这些命令安装好依赖之后才能真正安装具体的 Python 版本.


Install Specific Python Version
------------------------------------------------------------------------------
.. note::

    All python versions will be installed in: ~/.pyenv/versions.

.. code-block:: bash

    pyenv install 3.8.13

.. code-block:: bash

    pyenv install 3.9.12

.. code-block:: bash

    pyenv install 3.10.10

.. code-block:: bash

    pyenv install 3.11.6


.. _configure-pyenv-automatically:

Configure pyenv Automatically
------------------------------------------------------------------------------
.. code-block:: bash

    python3 cli.py install_pyenv


Reference
------------------------------------------------------------------------------
- `pyenv Github <https://github.com/pyenv/pyenv>`_
- `Install pyenv <https://github.com/pyenv/pyenv?tab=readme-ov-file#installation>`_
- `Common build problem <https://github.com/pyenv/pyenv/wiki/Common-build-problems>`_
- `Suggested build environment <https://github.com/pyenv/pyenv/wiki#suggested-build-environment>`_: 介绍了在不同的操作系统上 build Python 所需的依赖.
- `pyenv Commands <https://github.com/pyenv/pyenv/blob/master/COMMANDS.md>`_
