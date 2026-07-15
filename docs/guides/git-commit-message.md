# Git 提交信息

本仓库使用单文件 `commit-msg` hook 统一提交信息格式。

每个 clone 需要启用一次 hooks：

```powershell
git config core.hooksPath .githooks
```

提交信息必须使用以下格式：

```text
feat(scope): concise English summary

- English detail item.
- 中文说明：可选中文补充。
```

规则：

- 第一行必须使用 Conventional Commits。
- 允许的 type：`feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert`。
- 可选 scope 只能使用小写字母、数字和连字符，例如 `feat(ledfx): ...`。
- header 摘要必填，最长 72 字符。
- header 摘要建议保持英文，方便工具链和 changelog 稳定处理。
- 如果有正文，第二行必须为空行。
- 正文详情使用 `- ` bullet。
- 正文可以使用英文或中文。
- bullet 必须连续，中间不要插入空行。
- 较长 bullet 可以用两个空格缩进换行。
- 正文每行最长 100 字符。
- 不要把多个 bullet 写在同一行。

hook 故意不依赖 Python 或 Node，只使用 POSIX shell 和 `awk` 实现。
