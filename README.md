# MCU Firmware Agent Template

面向 **MCU 固件开发** 的模板仓库，默认以 Keil MDK 为真实构建入口，并把 agent 协作、交接文档、提交约束和可选硬件资料入口一起固定下来。

这个模板不管理上位机、Web、移动端、云服务或工厂 PC 工具。若产品包含这些软件，建议单独建仓库；本仓库只记录固件侧协议、接口和联调约束。

## 目录

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

## 新项目使用

1. 从此模板创建新仓库。
2. 修改 README、`docs/current/*` 和 `docs/requirements/*` 中的产品名与目标。
3. 把 MCU SDK、启动文件和 MDK 工程放进 `firmware/`。
4. 有硬件资料时，把原理图放到 `hardware/schematic/`。
5. 复制本机工具链配置：

```powershell
Copy-Item toolchain.example.json toolchain.local.json
```

6. 启用 hooks：

```powershell
git config core.hooksPath .githooks
```

7. 后续 agent 先读：

```text
AGENTS.md
docs/current/README.md
docs/current/state.md
docs/current/todo.md
docs/requirements/product-requirements.md
docs/guides/firmware-architecture.md
docs/guides/mcu-c-style.md
```

## 构建

MDK 是固件构建事实来源。脚本只做自动化封装，不替代 MDK 工程配置。

```powershell
python scripts/mdk_build.py
python scripts/mdk_clangd.py
```

`toolchain.local.json` 是本机文件，不提交。

## Boot / OTA

模板默认不启用 Boot/OTA，也不把 OTA 打包脚本放进根 `scripts/`。相关资料放在：

```text
examples/boot-ota/
```

需要时由具体产品复制、裁剪和实现。
