# Agent 运行约束

本文件约束 agent 在 Windows 主开发环境下如何执行命令和处理依赖。

## 命令执行

- 优先使用仓库脚本和 Python 标准库完成自动化任务。
- 复杂文件处理、批量路径处理、JSON/XML 解析、构建封装，优先写成 `scripts/*.py`。
- 不要把复杂逻辑写成一长串 PowerShell / pwsh 命令。
- `pwsh` 只用于简单检查命令，例如 `Get-Content`、`Get-ChildItem`、`git status`。
- 涉及路径拼接、递归扫描、批量删除/移动时，优先使用 Python 脚本，并显式校验目标路径。
- 不新增 Python 第三方依赖，除非用户明确同意。

## 推荐命令入口

```powershell
python -m unittest discover -s scripts/tests -v
python scripts/mdk_build.py
python scripts/mdk_clangd.py
python scripts/mdk_flash.py --require-hex
python scripts/mdk_clean.py --dry-run
git status --short --branch
git diff --check
```

- 多 `.uvprojx` 或多 target 时显式传 `--project` 和 `--target`。
- `mdk_clean.py --all` 使用前必须先执行 `--all --dry-run`。
- 参数和常见错误见 `docs/guides/mdk-toolchain-config.md`。

如果当前机器没有 `python` 命令，可以使用 Windows Python Launcher：

```powershell
py -3 scripts/mdk_build.py
py -3 scripts/mdk_clangd.py
py -3 scripts/mdk_flash.py --require-hex
py -3 scripts/mdk_clean.py --dry-run
```

## Windows 注意事项

- 路径中可能包含空格、中文和不同盘符，脚本必须使用 `pathlib.Path`。
- 本机配置放在 `toolchain.local.json`，不要写死用户本机路径。
- 不要依赖当前 shell 的临时变量、profile 或 alias。
- 不要要求用户切换 shell 才能完成基础任务。

## 依赖原则

- 模板仓库只依赖可解释、可复制的基础工具。
- Python 只要求 Python 3 和标准库，不锁具体小版本。
- 能用 Python 标准库完成的事情，不引入 Node、PowerShell 模块或 Python 第三方包。
- 产品项目确实需要额外工具时，必须写入 README 或对应指南。
