# MCU C Style

## Tools

- Use repository `.clang-format`.
- Use clangd for navigation and diagnostics.
- C standard: C99 unless the project states otherwise.

## Files

- C source files use `.c`; headers use `.h`.
- File names use lowercase with underscores.
- Each file should own one clear module or tightly related functionality.
- Headers expose only public types, macros, and function declarations.
- Headers must not define writable global variables.
- Each header must have an include guard.

## Naming

- Functions and variables: lowercase with underscores.
- Types: lowercase with underscores and `_t` suffix.
- Macros and enum values: uppercase with underscores.
- Public symbols must use a module prefix.
- Private static variables use `s_` prefix.
- Global variables use `g_` prefix.
- Time variables must include units, for example `timeout_ms`.

## Formatting

- 4 spaces indentation. No tabs.
- K&R braces: `if (cond) {`.
- All `if/else/for/while/do` bodies must use braces.
- One statement per line.
- Pointer declarations use `uint8_t *data`.
- Binary operators have spaces around them.

## Comments

- Code comments use English.
- Explain reasons, constraints, hardware notes, and protocol notes.
- Do not restate obvious code.
- Public functions should use Doxygen-style comments.
- Remove commented-out dead code before commit.

## Quality

- Declare and initialize local variables near the start of a function or block.
- Use fixed-width integer types for protocol, file format, and cross-module data.
- ISR-shared variables use `volatile` where needed.
- Validate input pointers or clearly document non-null requirements.
- Check return values from functions that return errors.
- Use `(void)` for intentionally ignored return values.
- Avoid `malloc/free` unless explicitly approved.
- Keep ISRs short.
- Avoid long blocking operations in normal tasks.
- `switch` must include `default`.
