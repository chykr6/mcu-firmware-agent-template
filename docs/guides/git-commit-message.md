# Git Commit Message

This repository uses a single-file `commit-msg` hook to keep commit messages consistent.

Enable hooks once per clone:

```powershell
git config core.hooksPath .githooks
```

Commit messages must use this format:

```text
feat(scope): concise English summary

- English detail item.
- 中文说明：可选中文补充。
```

Rules:

- The first line must use Conventional Commits.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Optional scope uses lowercase letters, digits, and hyphen, for example `feat(ledfx): ...`.
- Header summary is required and limited to 72 characters.
- Header summary should stay English for tooling and changelog stability.
- The second line must be blank when a body exists.
- Body detail items use `- ` bullets.
- Body can use English or Chinese.
- Bullet items must be consecutive, with no blank lines between them.
- Long bullet items may wrap onto continuation lines indented by two spaces.
- Body lines must be 100 characters or fewer.
- Do not put multiple bullet items on one line.

The hook intentionally avoids Python or Node dependencies. It is implemented as POSIX shell plus `awk`.
