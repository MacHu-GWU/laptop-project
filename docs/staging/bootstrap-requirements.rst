Development Machine Bootstrap Requirements
==============================================================================


Background
------------------------------------------------------------------------------
在现代软件开发工作流中, 开发者经常需要在新的机器上快速搭建开发环境. 无论是新购置的 Macbook Pro, 云端的 GitHub Codespaces, 还是 AWS EC2 实例, 都需要一套标准化的工具链来确保开发效率. 本文档描述了一个自动化 bootstrap 工具的需求和技术选型.


Target Platforms
------------------------------------------------------------------------------
本工具需要支持以下三种主要平台:

- **Macbook Pro** - macOS 操作系统, 本地开发环境
- **GitHub Codespaces** - 云端开发环境, 基于 Linux 容器
- **AWS EC2 with Amazon Linux** - 云主机环境, 生产级 Linux 发行版


Required Development Tools
------------------------------------------------------------------------------
工具安装的优先级和依赖关系如下:


Foundation Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. **mise-en-place** - 现代化的开发工具版本管理器, 作为整个工具链的基础
2. **base Python** (via mise) - Python 运行时环境, 由 mise 管理版本


Shell Enhancement Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
3. **starship.rs** - 跨平台的 shell prompt 增强工具, 提供美观的命令行提示符
4. **zsh-autosuggestions** - 命令自动补全建议
5. **zsh-syntax-highlighting** - 命令语法高亮
6. **zsh-completions** - 扩展的 zsh 补全功能
7. **zsh-autocomplete** - fish shell 风格的补全功能


Core Development Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
8. **uv** (via mise) - 极速的 Python 包管理器
9. **claude code** (via mise) - AI 辅助编程工具
10. **pnpm** (via mise) - 高效的 Node.js 包管理器


Python Environment Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
11. **python virtualenv** (via uv) - Python 虚拟环境管理
12. **ruff** (via uv) - 高性能 Python linter 和 formatter


Implementation Technology Choice
------------------------------------------------------------------------------


Why Python Instead of Shell Scripts?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
经过深思熟虑, 我们选择使用 Python 作为 bootstrap 工具的实现语言, 而非传统的 shell scripts. 主要原因如下:


Platform Availability
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
现代操作系统都预装了 Python:

- macOS 自带 Python (尽管版本可能较旧, 但足以运行 bootstrap 脚本)
- GitHub Codespaces 默认包含 Python
- Amazon Linux 预装 Python 3

这意味着我们可以直接使用 Python 而无需安装额外的运行时环境.


Mature Standard Library
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Python 标准库经过二十多年的发展, 已经非常成熟和稳定:

- ``subprocess`` 模块提供了可靠的进程管理和命令执行
- ``pathlib`` 提供了跨平台的路径操作
- ``json`` / ``toml`` (Python 3.11+) 支持配置文件解析
- ``urllib`` / ``http`` 提供了网络请求能力
- ``shutil`` 提供了文件系统操作


这些内置功能足以应对 bootstrap 过程中的所有需求.

Better Error Handling
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
相比 shell scripts, Python 提供了更完善的错误处理机制:

.. code-block:: python

   try:
       subprocess.run(['mise', 'install'], check=True, capture_output=True)
   except subprocess.CalledProcessError as e:
       print(f"Installation failed: {e.stderr.decode()}")
       # 可以进行更细粒度的错误恢复

Shell scripts 的错误处理通常依赖 ``set -e`` 或手动检查 ``$?``, 不够灵活和可读.

Cross-Platform Compatibility
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Python 代码在不同平台上的行为更加一致:

- 不需要担心 bash vs zsh vs sh 的差异
- 不需要处理 macOS 和 Linux 命令参数的细微差别
- ``os.name`` / ``sys.platform`` 提供了清晰的平台检测


Idempotency and State Management
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Python 更容易实现幂等性 (idempotency):

.. code-block:: python

   def ensure_mise_installed():
       if shutil.which('mise'):
           print("mise already installed, skipping...")
           return
       # 执行安装逻辑

幂等性确保了 bootstrap 脚本可以:

- 安全地多次运行
- 从失败的状态恢复
- 更新已安装的工具


Readability and Maintainability
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Python 代码更容易阅读和维护:

- 清晰的函数和模块组织
- 类型提示 (type hints) 提供文档和 IDE 支持
- 丰富的第三方库生态系统 (如果需要)


Performance Considerations
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
虽然 Python 的执行速度慢于 shell scripts, 但在 bootstrap 场景下这并不重要:

- **瓶颈在网络下载**, 不在脚本执行
- 下载 mise, uv, starship 等工具需要数秒到数十秒
- Python subprocess 的开销 (几十毫秒) 相比下载时间可以忽略不计

.. note::

   即使 Python 脚本比 shell 慢 100ms, 当下载一个 50MB 的工具需要 5 秒时, 这 100ms 的差异只占总时间的 2%, 完全可以接受.


One-Time Execution Context
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Bootstrap 是一次性操作, 不是频繁执行的任务:

- 新机器配置通常几周或几个月才发生一次
- 开发者愿意为可靠性和可维护性牺牲一点点速度
- 更重要的是确保安装过程可靠, 而不是快 0.5 秒


Design Principles
------------------------------------------------------------------------------
基于以上分析, bootstrap 工具应遵循以下设计原则:

1. **Idempotent Operations** - 所有安装操作都应该是幂等的, 可以安全地重复执行
2. **Graceful Degradation** - 如果某个工具安装失败, 不应阻止其他工具的安装
3. **Clear Progress Indication** - 提供清晰的进度反馈, 让用户知道当前正在安装什么
4. **Dependency-Aware** - 按照依赖顺序安装工具 (例如先安装 mise, 再通过 mise 安装其他工具)
5. **Platform Detection** - 自动检测运行平台, 执行相应的安装策略


Implementation Roadmap
------------------------------------------------------------------------------

Phase 1: Core Bootstrap Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 创建 ``bootstrap.py`` 主脚本
- 实现平台检测功能
- 实现 mise 安装逻辑

Phase 2: Tool Installation Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 实现各个工具的安装函数
- 确保依赖顺序正确
- 添加错误处理和重试逻辑

Phase 3: Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 生成工具配置文件 (如 ``.zshrc`` 配置)
- 设置环境变量
- 创建必要的目录结构

Phase 4: Testing and Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- 在三个目标平台上测试
- 验证幂等性
- 处理边界情况

Conclusion
------------------------------------------------------------------------------
通过使用 Python 实现 bootstrap 工具, 我们可以获得:

- **更好的可读性和可维护性**
- **更强的跨平台兼容性**
- **更完善的错误处理**
- **更容易实现幂等性**

虽然性能略逊于 shell scripts, 但在 bootstrap 这种以网络 I/O 为主的场景下, 这点性能差异完全可以忽略. Python 的成熟生态和清晰语法带来的长期收益, 远超过几百毫秒的执行时间差异.
