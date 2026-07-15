# Boot/OTA 需求

版本：v0.1
日期：YYYY-MM-DD
范围：只描述 Bootloader 和升级行为需求。

## 1. 目标

TBD

## 2. 升级通道

- USB MSC 拖拽升级：TBD
- USB CDC 协议升级：TBD
- 其他：TBD

## 3. Flash 布局

TBD

## 4. 升级包格式

TBD

## 5. 安全要求

- 跳转 APP 前校验向量表。
- 写入 APP 前校验升级包大小和 CRC。
- 避免启动写入不完整的 APP。
- 明确回滚或恢复行为。

## 6. 验收

TBD
