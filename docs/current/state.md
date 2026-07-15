# 当前状态

日期：2026-07-15

## 仓库状态

- 主分支：`main`
- 主远端：`origin`
- 备用远端：无 / TBD

## 固件目标

- MCU：TBD
- 构建入口：Keil MDK
- 主要输出：TBD
- 是否包含 Boot/OTA：否 / 是，见具体项目说明
- 是否使用 RTOS：否 / 是，见具体项目说明

## 架构边界

- 固件分层见 `docs/guides/firmware-architecture.md`。
- RTOS 约束见 `docs/guides/rtos-guidelines.md`。
- C 风格见 `docs/guides/mcu-c-style.md`。

## 当前实现

- 已提供 `mdk_build.py`、`mdk_flash.py`、`mdk_clean.py`、`mdk_clangd.py` 和 `mdk_common.py`
- 本机工具链通过被 Git 忽略的 `toolchain.local.json` 配置
- clangd 数据生成到仓库根目录，不生成编辑器专用配置
- clangd 参数从 `.uvprojx` 读取 CPU/FPU，并允许通过 `clangd.extra_flags` 覆盖
- 脚本测试位于 `scripts/tests/`

## 当前验证

- 脚本测试：`python -m unittest discover -s scripts/tests -v` 已通过
- 构建：模板不包含产品 `.uvprojx`，未执行固件构建
- 板上：未验证

## 当前风险

- 多 MDK 工程需要显式使用 `--project`，clangd 暂未合并多个工程数据库
