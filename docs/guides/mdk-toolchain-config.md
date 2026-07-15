# MDK 工具链配置

本模板不递归扫描系统盘查找 Keil。先复制本机配置模板：

```powershell
Copy-Item toolchain.example.json toolchain.local.json
```

再按本机安装路径编辑 `toolchain.local.json`：

```json
{
    "mdk": {
        "uv4_dir": "C:/Keil_v5/UV4"
    },
    "clangd": {
        "binary": "clang",
        "extra_flags": []
    }
}
```

- `toolchain.local.json` 是本机配置，已被 `.gitignore` 排除，禁止提交。
- 构建和 clangd 脚本不会使用 `toolchain.example.json` 作为实际配置。
- `mdk.uv4_dir` 必须指向 Keil 的 `UV4` 目录；命令行构建使用其中的 `uVision.com`。
- `clangd.binary` 指定 compilation database 中使用的 clang 可执行文件名。
- `clangd.extra_flags` 用于补充语言标准、ABI 或项目专用 clang 参数。

## 工程和 target 选择

脚本默认递归查找仓库内的 `.uvprojx`：

- 只有一个工程时自动选择。
- 存在多个工程时必须使用 `--project`。
- 工程只有一个 target 时自动选择。
- 存在多个 target 时必须使用 `--target`。

## 构建脚本

```powershell
python scripts/mdk_build.py
python scripts/mdk_build.py --rebuild
python scripts/mdk_build.py --project firmware/MDK-ARM/project.uvprojx --target APP
python scripts/mdk_build.py --uv4 C:/Keil_v5/UV4/uVision.com
```

`--rebuild` 使用 uVision `-r`。清理构建输出使用 `python scripts/mdk_clean.py`。

## clangd 脚本

```powershell
python scripts/mdk_clangd.py
python scripts/mdk_clangd.py --project firmware/MDK-ARM/project.uvprojx --target APP
```

脚本会从 `.uvprojx` 中读取指定 target 的 CPU/FPU、C 源文件、`Define` 宏和
`IncludePath`，并在仓库根目录输出：

```text
.clangd
compile_commands.json
```

脚本不生成 `.vscode` 等编辑器专用配置。VS Code、Zed、Neovim 等支持 clangd 的编辑器
可复用同一份 compilation database。

如果当前机器没有 `python` 命令，可以改用 `py -3`。
