# AGENTS.md

This file defines agent behavior only. Product requirements, current state, and TODO live under `docs/`.

## 1. Communication

- Use Chinese by default unless the user asks otherwise.
- Keep answers concise and conclusion first.
- Do not expand scope without user confirmation.
- When requirements are unclear, clarify before editing code.

## 2. Startup Reading Order

Before touching code in a new task, read:

1. `docs/current/README.md`
2. `docs/current/state.md`
3. `docs/current/todo.md`
4. Relevant files under `docs/requirements/`, `docs/firmware/`, and `docs/guides/`

## 3. Git

- Do not commit unless the user explicitly asks.
- Do not push unless the user explicitly asks.
- One commit must contain one clear topic.
- Before committing, update `docs/current/state.md` and `docs/current/todo.md` when the task changes project state.
- Explain which files will be committed and why they belong together.
- Do not commit build outputs, IDE user files, temporary files, local tool paths, or unrelated formatting.
- Do not rewrite history or force push unless explicitly requested.
- Commit messages must follow `docs/guides/git-commit-message.md`.
- Enable hooks once per clone: `git config core.hooksPath .git-hooks`.

## 4. Workspace Safety

- The working tree may contain user changes. Preserve them.
- Do not revert user changes unless explicitly requested.
- Read files before editing them.
- Prefer `rg` / `rg --files` for search.
- Use small, focused edits.
- Keep generated files out of git unless explicitly documented.

## 5. MDK Project Files

- MDK `.uvprojx` is source controlled and must be treated carefully.
- Before modifying `.uvprojx`, inspect the diff and ensure build options, macros, include paths, output names, and flash settings are not accidentally reset.
- `.uvoptx`, `.uvgui*`, and local debug configuration are user/local files by default and should not be committed.
- MDK group naming rules live in `docs/guides/mdk-project-groups.md`.

## 6. Verification

- If code changes can be built, run the build before claiming completion.
- If build cannot run, explain why.
- Documentation-only changes require at least `git diff` and `git status` inspection.
- Do not say “should work” when it was not verified.
- MCU hardware behavior needs board verification; clearly separate build verification from board verification.

## 7. MCU C Style

Follow `docs/guides/mcu-c-style.md` and the repository `.clang-format`.
