# 固件架构指南

本文件约束 MCU 固件的分层和依赖方向，适用于裸机和 RTOS 项目。

## 1. 推荐层次

```text
app/          产品业务、用户功能、状态机、模式管理
services/     可复用服务，如 storage、log、event、time、settings
protocol/     协议解析、命令分发、帧编解码
bsp/          板级驱动，贴硬件，不写产品业务
drivers/      芯片厂库、CMSIS、启动文件，尽量少改
middleware/   FatFs、USB、RTOS、CherryRB、MultiButton 等通用组件
```

实际目录可以按项目调整，但职责边界必须清楚。

## 2. 依赖方向

推荐方向：

```text
app -> services -> bsp -> drivers
app -> protocol
app -> middleware wrappers
protocol -> app public control API
services -> bsp / middleware
bsp -> drivers
```

禁止方向：

- `bsp` include 或调用 `app`。
- `drivers` include 产品业务头文件。
- 通用 `middleware` include 产品业务头文件。
- 协议层直接修改业务模块内部静态状态。
- ISR 中直接执行复杂业务流程。

## 3. BSP

BSP 只表达“这块板怎么驱动硬件”。

允许：

- GPIO、UART、SPI、I2C、DMA、timer、flash、LED IC、按键扫描底层。
- 必要的硬件时序、寄存器配置、DMA buffer。

不允许：

- 产品模式切换。
- 文件格式解析。
- 用户协议语义。
- 持久化策略。

## 4. App

App 层表达产品行为。

允许：

- 模式管理。
- 用户输入处理。
- 播放/控制策略。
- 错误提示策略。
- 参数持久化策略。

不建议：

- 直接写寄存器。
- 直接操作复杂外设细节。
- 到处 include BSP 私有头。

## 5. Protocol

协议层负责输入输出格式，不拥有产品状态。

推荐做法：

- parser 校验帧格式、长度、CRC、参数范围。
- command dispatch 调用 app 公开 API。
- 错误码映射集中管理。

禁止：

- 协议层绕过 app API 直接改模式内部上下文。
- parser 调用 start/stop/restart 这类播放器内部控制，除非这是 app 公共 API。

## 6. Middleware

中间件优先保持通用，不向产品业务回调硬编码。

如需适配产品：

- 建 wrapper 或 port 层。
- wrapper 可以在 app/services 下。
- middleware 原始源码尽量不直接改。

## 7. 中断与任务

- ISR 尽量短，只清标志、搬数据、投递事件或唤醒任务。
- 主循环或 task 处理业务。
- 长耗时操作必须有明确调度策略。
- USB、FatFs、Flash、日志等共享资源必须定义互斥或串行入口。

## 8. 公共头文件

公共头文件只暴露外部需要的 API。

- 私有状态放 `.c` 文件静态变量。
- 跨模块数据结构保持小而清晰。
- 不在公共头文件暴露硬件无关模块不需要的 BSP 类型。
