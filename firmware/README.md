# 固件目录

把 MCU 固件工程放在这里。

模板不强制固定 APP / Boot 目录形态。常见放法：

```text
firmware/MDK-ARM/
firmware/User/
firmware/Drivers/
firmware/Middlewares/
```

如果产品包含 APP + Boot，可以在 `firmware/MDK-ARM/` 下维护两个 target，也可以采用产品专用目录结构，但必须在 `docs/current/state.md` 说明清楚。
