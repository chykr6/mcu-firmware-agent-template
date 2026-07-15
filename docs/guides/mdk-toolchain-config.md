# MDK Toolchain Config

Copy `toolchain.example.json` to `toolchain.local.json` and edit local paths.

`toolchain.local.json` must not be committed.

Example fields:

- `uv4`: Keil uVision executable.
- `fromelf`: ARM fromelf executable.
- `project`: MDK project path.
- `target`: MDK target name.
