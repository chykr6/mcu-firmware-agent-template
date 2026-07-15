# MDK 工程分组

使用稳定的 group 名称，方便人和 agent 安全编辑 `.uvprojx`。

推荐分组：

```text
User/app
User/app/<feature>
User/bsp/<driver>
User/protocol
User/usb
Middlewares/<name>
Drivers/CMSIS
Drivers/Vendor
```

规则：

- 移动文件所属 group 时，不得顺手改变编译选项。
- 编辑文件列表时，不得重置 target 选项。
- startup、system、scatter、flash 配置必须保持显式可查。
