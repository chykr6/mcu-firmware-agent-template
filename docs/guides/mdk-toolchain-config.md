# MDK 工具链与脚本使用

本模板提供 Keil MDK 构建、clangd 数据生成、烧录和清理脚本。产品仓库应在 README 和
`docs/current/state.md` 补充真实 MCU、工程路径、target 和验证结果。

## 1. 本机配置

```powershell
Copy-Item toolchain.example.json toolchain.local.json
```

编辑被 Git 忽略的 `toolchain.local.json`：

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

- `toolchain.example.json` 只描述字段，不用于实际构建。
- `mdk.uv4_dir` 指向包含 `uVision.com` 的目录。
- `clangd.binary` 写入 compilation database。
- `clangd.extra_flags` 补充语言标准、ABI 或项目专用 clang 参数。
- 不在仓库、脚本或文档中写死开发者本机路径。

## 2. 工程和 target 选择

脚本从当前目录向下查找 `.uvprojx`：

- 唯一工程和唯一 target 可以自动选择。
- 多工程时使用 `--project`。
- 多 target 时使用 `--target`。

示例：

```powershell
python scripts/mdk_build.py --project firmware/app/MDK-ARM/app.uvprojx --target APP
python scripts/mdk_build.py --project firmware/boot/MDK-ARM/boot.uvprojx --target BOOT
```

`mdk_clangd.py` 当前一次生成一个工程的数据库。切换工程时重新运行并覆盖根目录数据库，
避免混合不同 target 的宏和 include path。

## 3. mdk_build.py

```powershell
python scripts/mdk_build.py
python scripts/mdk_build.py --rebuild
```

| 参数 | 说明 |
| --- | --- |
| `--project PATH` | 指定 `.uvprojx` |
| `--target NAME` | 指定 target |
| `--uv4 PATH` | 临时覆盖 `uVision.com` 或 `UV4.exe` |
| `--rebuild` | 完整重构建 |
| `--log PATH` | 覆盖构建日志路径 |
| `--tail N` | 设置日志尾行数，默认 80 |

脚本同时检查 uVision 返回码和日志中的 error 数量。

## 4. mdk_clangd.py

```powershell
python scripts/mdk_clangd.py
```

默认在仓库根目录生成：

```text
.clangd
compile_commands.json
```

| 参数 | 说明 |
| --- | --- |
| `--project PATH` | 指定 `.uvprojx` |
| `--search-root PATH` | 自动发现工程的起始目录 |
| `--target NAME` | 指定 target |
| `--workspace-root PATH` | 指定生成物目录 |
| `--output PATH` | 指定 compilation database 路径 |
| `--compiler NAME` | 覆盖 `clangd.binary` |
| `--no-clangd` | 不写 `.clangd` |

脚本读取 target 的 CPU/FPU、C 源文件、宏、include path 和 misc controls。无法可靠从 MDK
转换的参数应放入 `clangd.extra_flags`，不要写死到通用脚本。

脚本不生成 `.vscode`、Zed 或其他编辑器专用配置。

## 5. mdk_flash.py

```powershell
python scripts/mdk_flash.py --require-hex
```

| 参数 | 说明 |
| --- | --- |
| `--project PATH` | 指定 `.uvprojx` |
| `--target NAME` | 指定 target |
| `--uv4 PATH` | 临时覆盖 uVision 可执行文件 |
| `--log PATH` | 覆盖烧录日志 |
| `--tail N` | 设置失败日志尾行数 |
| `--require-hex` | 烧录前检查预期 HEX |

脚本使用 target 已配置的下载算法和调试器，不生成本机 probe 配置。

## 6. mdk_clean.py

```powershell
python scripts/mdk_clean.py --dry-run
python scripts/mdk_clean.py
```

| 参数 | 说明 |
| --- | --- |
| `--project PATH` | 指定 `.uvprojx` |
| `--target NAME` | 指定 target |
| `--dry-run` | 只显示清理范围 |
| `--all` | 额外删除 `.uvoptx`、`.uvguix.*` 等用户配置 |

使用 `--all` 前必须先运行 `--all --dry-run`。

## 7. 脚本测试

```powershell
python -m unittest discover -s scripts/tests -v
```

脚本测试不等于产品固件构建。模板没有真实 `.uvprojx` 时，只能声称脚本测试通过。

## 8. 常见错误

- `toolchain config not found`：复制并编辑 `toolchain.local.json`。
- `uVision.com not found`：检查 `mdk.uv4_dir`。
- multiple projects/targets：使用 `--project`、`--target`。
- HEX 不存在：先构建并确认 target 开启 HEX 输出。
- clangd 参数不完整：检查 `.uvprojx`，必要时补充 `clangd.extra_flags`。

没有 `python` 命令时，可将上述命令替换为 `py -3`。
