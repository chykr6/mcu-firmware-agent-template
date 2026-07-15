# MCU 固件 Agent 模板

这是面向 **MCU 固件开发** 的模板仓库。它默认以 Keil MDK 为真实构建入口，并把 agent 协作、交接文档、提交约束和可选硬件资料入口固定下来。

这个模板不管理上位机、Web、移动端、云服务或工厂 PC 工具。若产品包含这些软件，建议单独建仓库；本仓库只记录固件侧协议、接口和联调约束。

## 模板包含什么

```text
firmware/              固件代码入口，具体项目自行放 MDK 工程、User、Drivers、Middlewares
hardware/              可选硬件资料入口，建议至少放原理图
  schematic/           原理图 PDF 或源文件，推荐每个板级项目都有
  pcb/                 PCB 源文件或导出资料，可选
  production/          Gerber、BOM、坐标文件、生产说明，可选
docs/                  需求、当前状态、固件说明、长期指南
scripts/               通用 MDK/clangd 辅助脚本，不放产品业务脚本
examples/              可选方案示例，例如 Boot/OTA
tests/                 脚本或工具层测试，默认不承载 MCU 业务测试
.githooks/             提交和格式检查 hook
```

## 用作产品仓库后怎么改 README

从模板创建产品仓库后，根 `README.md` 不应继续介绍模板本身，而应该改成产品入口。建议至少包含：

- 产品名称、型号、用途和核心能力。
- MCU、构建工具、烧录/调试方式。
- 固件目录、MDK 工程位置、主要 target。
- 一键构建、生成 clangd、烧录或产物导出的命令。
- 硬件资料位置，至少说明原理图在哪里。
- agent 开始任务前应阅读的文档列表。
- 当前不支持或暂缓的范围，例如上位机、Boot/OTA、量产工具等。

产品 README 写产品事实；模板规则、编码规范和 agent 约束继续放在 `AGENTS.md` 和 `docs/guides/`。

## 新项目初始化

1. 从此模板创建新仓库。
2. 立刻把根 `README.md` 改成产品 README。
3. 修改 `docs/current/*` 和 `docs/requirements/*` 中的产品名与目标。
4. 把 MCU SDK、启动文件和 MDK 工程放进 `firmware/`。
5. 有硬件资料时，把原理图放到 `hardware/schematic/`。
6. 复制本机工具链配置：

```powershell
Copy-Item toolchain.example.json toolchain.local.json
```

7. 启用 hooks：

```powershell
git config core.hooksPath .githooks
```

8. 后续 agent 先读：

```text
AGENTS.md
docs/current/README.md
docs/current/state.md
docs/current/todo.md
docs/requirements/product-requirements.md
docs/guides/agent-runtime.md
docs/guides/firmware-architecture.md
docs/guides/mcu-c-style.md
```

## 构建和 clangd

MDK 是固件构建事实来源。脚本只做自动化封装，不替代 MDK 工程配置。

```powershell
python scripts/mdk_build.py
python scripts/mdk_build.py --rebuild
python scripts/mdk_clangd.py
```

- `scripts/mdk_build.py`：读取 `toolchain.local.json`，调用 uVision 命令行构建指定 target。
- `scripts/mdk_clangd.py`：读取 `.uvprojx`，生成 clangd 使用的 `compile_commands.json` 和 `.clangd`。
- `scripts/mdk_common.py`：公共配置、路径和命令执行工具，不直接运行。

`toolchain.local.json` 是本机文件，不提交。

## 仓库依赖

基础依赖：

- Git：版本管理和 hooks。
- Python 3：运行 `scripts/` 下的仓库脚本，只使用标准库，不锁具体小版本。
- Keil MDK / uVision：真实固件构建入口。
- clangd：可选，用于代码导航和基础诊断。
- POSIX shell + `awk`：运行 `.githooks/commit-msg`，Git for Windows 自带即可。

可选工具：

- `rg`：快速搜索。
- `clang-format`：按仓库 `.clang-format` 格式化 C/C++ 文件。

不默认依赖 Node、PowerShell 模块、Python 第三方包或上位机工具链。

如果 Windows 环境没有把 `python` 放进 PATH，可以使用 `py -3` 运行同一批脚本。

## Boot / OTA

模板默认不启用 Boot/OTA，也不把 OTA 打包脚本放进根 `scripts/`。相关资料放在：

```text
examples/boot-ota/
```

需要时由具体产品复制、裁剪和实现。
