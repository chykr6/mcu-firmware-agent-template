# MCU Firmware Agent Template

A workflow template for MCU firmware projects developed with Keil MDK and coding agents.

The template focuses on firmware engineering first: MDK project structure, agent handoff rules, current-state documents, requirements, commit hooks, and optional Boot/OTA support. Hardware files are included only as firmware context, so schematics and production references can live with the firmware when useful. PC tools, desktop apps, web apps, and upper-computer software should usually be managed in separate repositories.

## Layout

```text
firmware/              Main MCU application firmware
  MDK-ARM/             Keil MDK project files
  User/                Application, BSP, protocol, USB, product logic
  Drivers/             Vendor CMSIS and peripheral libraries
  Middlewares/         Third-party middleware
boot/                  Optional bootloader firmware, enabled when OTA is needed
hardware/              Optional hardware references for firmware work
  schematic/           Schematic PDF/source, recommended for every board project
  pcb/                 PCB source or layout exports, optional
  production/          Gerber, BOM, placement files, optional
docs/                  Requirements, firmware notes, current state, guides
scripts/               Build, clangd, package and release helpers
.githooks/             Repository hooks
```

## Start A New Firmware Project

1. Create a new repository from this template.
2. Rename product identifiers in README and docs.
3. Copy vendor SDK, startup files, and MDK project into `firmware/`.
4. Put the schematic PDF or source file under `hardware/schematic/` when available.
5. Copy `toolchain.example.json` to `toolchain.local.json` and edit local paths.
6. Enable hooks:

```powershell
git config core.hooksPath .githooks
```

7. Read in order:

```text
AGENTS.md
docs/current/README.md
docs/current/state.md
docs/current/todo.md
docs/requirements/product-requirements.md
docs/guides/mcu-c-style.md
```

## Build

Keil MDK is the source of truth for embedded builds.

```powershell
python scripts/mdk_build.py
python scripts/mdk_clangd.py
```

Scripts are intentionally conservative. Adapt `toolchain.local.json` and project paths before use.

## Scope

This template is for MCU firmware repositories. If a project also has an upper-computer app, mobile app, factory tool, or cloud service, keep that software in a dedicated repository and document only the firmware-facing protocol here.
