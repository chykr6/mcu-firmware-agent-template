# MDK Project Groups

Use stable group names so humans and agents can edit `.uvprojx` safely.

Recommended groups:

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

Rules:

- Moving files between groups must not change compiler options.
- Do not reset target options while editing file lists.
- Keep startup, system, scatter, and flash settings explicit.
