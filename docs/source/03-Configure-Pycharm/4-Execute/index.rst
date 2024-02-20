Execute
==============================================================================
此文档重点介绍了如何在 PyCharm 中运行脚本.

- Run Last Executed File: ``Ctrl + R`` (MacOS)
- Select a file to Run: ``Ctrl + Alt + R`` (MacOS)


Set your Python executable (Even for virtualenv)
------------------------------------------------------------------------------
如何用快捷键来用指定的 Python 解释器运行脚本.

``Preference`` -> ``Project`` -> ``Project Interpreter``, Set Python executable.

Windows:

- ``C:\Python27\python.exe``

MacOS:

If your python are installed from `HomeBrew <https://brew.sh/>`_, it should be at:

- ``/usr/local/Cellar/python2/2.7.13/Frameworks/Python.framework/Versions/2.7/bin/python2.7``

Linux:

- ``<path-to-your-virtualenv-folder>``


Execute in Bash
------------------------------------------------------------------------------
.. note::

    Before 2020, we need a `BashSupport <https://plugins.jetbrains.com/plugin/4230-bashsupport>`_ plugin (No longer free). But after that, PyCharm support run bash script out-of-the-box.

Another way is to use ``External Tools`` to configure it.

1. Set up external tools: ``Preference`` -> ``Tools`` -> ``External Tools`` -> ``Add new one`` click ``+`` sign.
2. Config executable: ``Name``: name for this tool, I use ``Run with Bash``, ``Description``: any description text, ``Program``: The executable file (.exe for Windows, usually using git-bash.exe, /bin/bash for MacOS), ``Parameters``: ``$FileName$`` (you can select from macro), ``Working Directory``: ``$FileDir$``, click ``OK``.
3. Assign a Keymap: ``Preference`` -> ``Keymap`` -> Search ``Run with Bash`` -> Add a keymap, I use ``Shift + ```.
4. Try it out: select a file in project view, press Ctrl + Shift + `````.


Open File in Sublime Text
------------------------------------------------------------------------------
1. Set up external tools: ``Preference`` -> ``Tools`` -> ``External Tools`` -> ``Add new one`` click ``+`` sign.
2. Config executable: ``Name``: name for this tool, I use ``Sublime Text``, ``Description``: any description text, ``Program``: The sublime text executable file (``path\to\Sublime Text.exe`` for Windows, ``/Applications/Sublime Text.app`` for MacOS), ``Parameters``: ``$FileName$`` (you can select from macro), ``Working Directory``: ``$FileDir$``, click ``OK``.
3. Assign a Keymap: ``Preference`` -> ``Keymap`` -> Search ``Sublime Text`` -> Add a keymap, I use ``Alt + Cmd + S``.
4. Try it out: select a file in project view, press ``Alt + Cmd + S``.

.. note::

    Configuration for VSCode is similar.

Reference:

- PyCharm: Open the current file in Vim, Emacs or Sublime Text: https://andrewbrookins.com/python/open-the-current-file-in-vim-emacs-or-sublime-text-from-pycharm/
