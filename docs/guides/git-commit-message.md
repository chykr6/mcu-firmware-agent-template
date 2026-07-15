# Git Commit Message

This repository uses a `commit-msg` hook to keep commit messages consistent.

Enable it once per clone:

```powershell
git config core.hooksPath .git-hooks
```

Commit messages must use this format:

```text
feat(scope): concise summary

- First detail item.
- Second detail item.
- Third detail item.
```

Rules:

- The first line must use Conventional Commits.
- The second line must be blank when a body exists.
- Body detail items use `- ` bullets.
- Bullet items must be consecutive, with no blank lines between them.
- Do not put multiple bullet items on one line.
