# RTOS 指南

本文件用于约束接入 RTOS 后的固件结构。裸机项目可保留本文件作为后续参考。

## 1. 基本原则

- RTOS 不是把每个模块都变成 task。
- task 必须服务于明确的并发边界、阻塞等待或实时性需求。
- 能用事件驱动/队列串行化的资源，不用多个 task 直接抢。

## 2. Task 设计

每个 task 必须在文档中说明：

- 名称
- 职责
- 优先级
- 栈大小
- 输入事件/队列
- 输出动作
- 允许阻塞的 API
- 不能调用的 API

推荐命名：

```text
app_task
usb_task
storage_task
protocol_task
log_task
```

## 3. 优先级

- 中断响应由 ISR 保证，不用高优先级 task 代替 ISR。
- 通信 RX/TX、USB、存储、日志、UI 分开评估优先级。
- 低优先级 task 不得长期持有高优先级 task 需要的锁。

## 4. 栈

- 每个 task 必须有栈预算和验证记录。
- 大 buffer 不默认放 task 栈。
- 大局部结构体要评估是否改为静态、共享 scratch 或分块处理。

## 5. ISR 到 Task

允许：

- event flag
- semaphore
- queue
- ring buffer + notify

不允许：

- ISR 中调用 FatFs、printf、大量日志、malloc/free、复杂状态机。

## 6. 共享资源

必须定义所有权或互斥策略：

- Flash / EEPROM
- FatFs / filesystem
- USB device/host
- UART protocol
- pixel output DMA
- logging backend

## 7. 时间 API

- 统一使用项目封装的 time/tick API。
- 不在业务层散落 RTOS 原始 tick 换算。
- 时间变量必须带单位后缀，例如 `timeout_ms`。

## 8. 日志

- 日志后端必须说明线程安全策略。
- ISR 日志默认禁止。
- 高频路径日志必须有宏开关或限频。

## 9. 裸机迁移到 RTOS

迁移时优先保持模块 API 稳定，只替换调度入口：

```text
bare-metal poll/tick -> RTOS task/event
```

不要在迁移时顺手重写业务语义。
