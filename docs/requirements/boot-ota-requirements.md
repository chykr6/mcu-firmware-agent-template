# Boot OTA Requirements

Version: v0.1
Date: YYYY-MM-DD
Scope: Bootloader and update behavior requirements only.

## 1. Goal

TBD

## 2. Update Transport

- USB MSC drag-and-drop: TBD
- USB CDC protocol: TBD
- Other: TBD

## 3. Flash Layout

TBD

## 4. Package Format

TBD

## 5. Safety Requirements

- Validate vector table before booting app.
- Validate package size and CRC before writing app.
- Avoid booting a partially written app.
- Define rollback or recovery behavior.

## 6. Acceptance

TBD
