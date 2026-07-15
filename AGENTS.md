# AGENTS.md

本文件只约束 agent 开发行为。产品需求、当前状态、TODO 不写在这里，避免过期。

## 1. 沟通

- 默认使用中文。
- 回答短，先给结论。
- 不做用户没要求的扩展设计。
- 需求不清楚时先问，不要直接改代码。

## 2. 开始任务前先读

1. `docs/current/README.md`
2. `docs/current/state.md`
3. `docs/current/todo.md`
4. 与任务相关的 `docs/requirements/`、`docs/firmware/`、`docs/hardware/`、`docs/guides/`

## 3. Git

- 不允许主动提交；只有用户明确说“提交 / commit / git commit”后才提交。
- 不允许主动 push，除非用户明确要求。
- 一个提交只包含一个清晰主题。
- 提交前必须更新与本次任务相关的 `docs/current/state.md` 和 `docs/current/todo.md`；如果无需更新，要说明原因。
- 提交前说明将提交哪些文件，以及为什么属于同一主题。
- 不提交构建输出、IDE 用户文件、临时文件、本机路径配置或无关格式化。
- 不改写历史，不 force push，不做破坏性 git 操作，除非用户明确要求。
- 提交信息必须符合 `docs/guides/git-commit-message.md`。
- 每个 clone 启用 hook：`git config core.hooksPath .githooks`。

## 4. 工作区安全

- 工作区可能有用户未提交改动；必须保留。
- 不 revert 用户改动。
- 编辑前先读取相关文件现状。
- 优先用 `rg` / `rg --files` 搜索。
- 未经用户明确允许，不递归搜索仓库外目录或系统盘。
- 手工编辑保持小范围、单主题。
- 生成文件默认不入库，除非文档明确允许。

## 5. 命令和脚本

- 主开发环境是 Windows，但不要把复杂任务写成 `pwsh` 长命令。
- 自动化任务优先使用仓库内 Python 脚本。
- `pwsh` 只用于简单检查命令，不用于复杂文件处理、路径拼接或批量改动。
- 具体规则见 `docs/guides/agent-runtime.md`。

## 6. MDK 工程文件

MDK 工程规则见 `docs/guides/mdk-toolchain-config.md` 和 `docs/guides/mdk-project-groups.md`。AGENTS.md 不重复两份指南的内容。

## 7. 固件分层

固件分层和依赖方向见 `docs/guides/firmware-architecture.md`。裸机和 RTOS 项目都必须遵守该文件定义的边界。

## 8. RTOS

如果项目接入 RTOS，先阅读并补充 `docs/guides/rtos-guidelines.md`。不要把裸机轮询习惯直接搬进 RTOS task。

## 9. 硬件资料

- 硬件文件只是固件开发上下文，不是本模板的主交付物。
- 建议至少把原理图 PDF 或源文件放到 `hardware/schematic/`。
- 只有需要解释硬件设计时，才写 `docs/hardware/`。
- 新增或修改 SVG/框图前，先读 `docs/guides/diagram-style.md`。

## 10. 验证

- 声称完成前必须做对应验证。
- 能构建就构建；不能构建要说明原因。
- 文档改动至少检查 diff 和 git status。
- 不用“应该可以”代替验证结果。
- MCU 板上行为要明确区分“已构建”和“已上板验证”。

## 11. C 风格

编码风格以 `docs/guides/mcu-c-style.md` 和仓库 `.clang-format` 为准。
