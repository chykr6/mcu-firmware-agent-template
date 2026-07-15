# 固件说明

本目录用于记录固件实现相关说明。

基础模板只保留通用入口，不预设旧固件迁移、新固件实现笔记等产品业务文档。具体产品可以按需要新增，例如：

```text
module-xxx.md
protocol-xxx.md
bring-up-notes.md
```

当前保留文件：

- `app-changelog.md`：APP 固件版本记录。

Boot/OTA 不是基础模板默认能力；需要时参考 `examples/boot-ota/`。
