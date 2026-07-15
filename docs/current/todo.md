# TODO

## P0

- [ ] 建立 MDK 工程基线。
- [ ] 确认 `python scripts/mdk_build.py` 可构建。
- [ ] 生成 clangd 数据库。
- [ ] 确认下载/调试链路。
- [ ] 补齐产品需求。

## P1

- [ ] 明确固件分层和模块边界。
- [ ] Bring-up BSP 和中间件。
- [ ] 建立最小 main loop 或 RTOS task 骨架。

## 暂缓

- [ ] Boot/OTA。如需要，参考 `examples/boot-ota/`。

## 约束

- MDK 工程改动必须谨慎检查 diff。
- 提交前同步 current 状态。
