# Agent 快速接手指南

本文提供 MCU 固件项目的通用接手流程和可复制提示词。具体产品事实必须由产品仓库的
`docs/requirements/`、`docs/current/` 和实际源码提供。

## 1. 接手原则

- 第一次接手默认只读，不修改、不格式化、不提交。
- 先检查 Git 工作区，保留所有用户未提交改动。
- 产品事实看 requirements，当前状态看 current，长期边界看 guides。
- 文档必须与源码和工程文件交叉核对，不假设文档永远最新。
- 区分脚本测试、固件构建、下载成功和板上功能验证。
- 未确认硬件连接、probe 和端口前，不执行烧录或串口操作。

## 2. 只读接手顺序

1. `AGENTS.md`
2. `docs/current/README.md`
3. `docs/current/state.md`
4. `docs/current/todo.md`
5. `docs/requirements/` 中的产品需求或能力基线
6. `docs/firmware/` 和任务相关 `docs/guides/`
7. `git status --short --branch`
8. 最近提交
9. `.uvprojx`、target 和工具链配置
10. `scripts/` 命令入口及 `--help`
11. main、tick/ISR 和主循环入口
12. 与当前任务相关的源码调用链

接手报告至少覆盖：

- 产品和 MCU；
- 工程、target、构建和烧录入口；
- 调度模型；
- 关键模块及依赖边界；
- 已实现和已验证范围；
- TODO、风险和限制；
- 工作区未提交改动；
- 建议的下一步。

## 3. 通用只读接手提示词

```text
请先只读接手当前 MCU 固件项目，不修改文件、不格式化、不提交、不 push。

严格遵守仓库 AGENTS.md。依次阅读：
1. docs/current/README.md
2. docs/current/state.md
3. docs/current/todo.md
4. docs/requirements/ 中与产品相关的需求或能力基线
5. 与当前实现相关的 docs/firmware/ 和 docs/guides/

然后检查：
- git status --short --branch
- 最近 8 个提交
- 仓库内所有 .uvprojx 和 target
- toolchain.example.json
- scripts/ 下的 MDK 工具入口及 --help
- main、1 ms tick/ISR、主循环或 RTOS task 入口
- 当前任务相关模块的主要调用链和依赖方向

不要假设文档一定最新，请用实际源码和工程文件交叉核对。请用中文简短报告：
1. 产品和 MCU
2. 工程、target、工具链配置和构建命令
3. 调度模型和启动流程
4. 关键模块及依赖方向
5. 当前已实现能力
6. 脚本测试、构建、下载和板上验证分别做到哪里
7. 当前 TODO、风险和限制
8. 工作区未提交改动
9. 建议的下一步
```

## 4. 通用继续开发提示词

```text
请继续当前 MCU 固件任务。先读取 AGENTS.md、docs/current/state.md、
docs/current/todo.md、产品需求和任务相关源码，再开始修改。

要求：
- 保留用户未提交改动，不 revert 无关文件。
- 修改前检查现状、调用链和工程配置，不凭旧文档猜测。
- 遵守仓库固件分层和 BSP/业务依赖边界。
- 修改 .uvprojx 前保留 target 编译选项、宏、include、输出和下载配置。
- 手工改动保持小范围、单主题，不做未要求的扩展设计。
- 完成后运行脚本测试和项目规定的构建命令。
- 明确区分脚本测试、已构建、已下载和已上板验证。
- 不主动 commit 或 push；只有我明确要求时才执行。

交付时报告：修改文件、行为变化、验证命令与结果、未验证项和后续风险。
```

## 5. 模板落地要求

从模板创建产品仓库后，应立即：

- 将提示词中的通用路径替换为真实产品基线；
- 在 `docs/current/state.md` 写明工程、target、MCU 和验证状态；
- 在 `docs/firmware/` 写真实运行入口和模块边界；
- 删除不适用于该产品的占位描述；
- 保持本指南只描述接手方法，不堆积产品 TODO。
