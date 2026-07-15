# MDK 工具链配置

将 `toolchain.example.json` 复制为 `toolchain.local.json`，然后修改本机路径。

`toolchain.local.json` 是本机配置，禁止提交。

字段：

- `uv4`：Keil uVision 可执行文件路径，用于命令行构建。
- `fromelf`：ARM fromelf 可执行文件路径，供产品项目后续导出产物时使用。
- `project`：MDK 工程路径，通常是 `.uvprojx`。
- `target`：默认构建和生成 clangd 数据库的 MDK target 名称。

## 构建脚本

```powershell
python scripts/mdk_build.py
python scripts/mdk_build.py --rebuild
python scripts/mdk_build.py --clean
python scripts/mdk_build.py --target APP
```

脚本会调用：

```text
UV4.exe -b <project> -t <target> -o <log>
```

`--rebuild` 使用 `-r`，`--clean` 会先执行 `-c`。

## clangd 脚本

```powershell
python scripts/mdk_clangd.py
python scripts/mdk_clangd.py --target APP
```

如果当前机器没有 `python` 命令，可以改用 `py -3`。

脚本会从 `.uvprojx` 中读取指定 target 的：

- C 源文件列表。
- `Define` 宏。
- `IncludePath` 头文件路径。

输出：

```text
<MDK工程目录>/compile_commands.json
.clangd
```

这个数据库用于 clangd 导航和基础诊断，不保证完全复刻 ARMCC/AC6 的所有私有编译参数。产品项目如果需要更精确的参数，可以在此脚本上继续增强。
