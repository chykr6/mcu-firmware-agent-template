# MDK MCU Template

A reusable workflow template for Keil MDK based MCU firmware projects.

This template is designed for projects developed by humans and coding agents together. It standardizes project layout, agent handoff documents, MDK build scripts, commit rules, and optional Boot/OTA structure.

## Layout

```text
firmware/              Main application firmware project
  MDK-ARM/             Keil MDK project files
  User/                Application, BSP, protocol, USB, product logic
  Drivers/             Vendor CMSIS and peripheral libraries
  Middlewares/         Third-party middleware
boot/                  Optional bootloader project
scripts/               Build, clangd, package and release helpers
docs/                  Requirements, firmware notes, current state, guides
.git-hooks/            Repository hooks
```

## Start A New Product

1. Create a new repository from this template.
2. Rename product identifiers in README and docs.
3. Copy vendor SDK, startup files, and MDK project into `firmware/`.
4. Copy `toolchain.example.json` to `toolchain.local.json` and edit local paths.
5. Enable hooks:

```powershell
git config core.hooksPath .git-hooks
```

6. Read in order:

```text
AGENTS.md
docs/current/README.md
docs/current/state.md
docs/current/todo.md
docs/requirements/product-requirements.md
docs/guides/mcu-c-style.md
```

## Build

The template expects MDK to be the source of truth for embedded builds.

```powershell
python scripts/mdk_build.py
python scripts/mdk_clangd.py
```

Scripts are intentionally conservative. Adapt `toolchain.local.json` and project paths before use.

## Agent Rule

Do not start coding before reading `AGENTS.md` and `docs/current/*`.
