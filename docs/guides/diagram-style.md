# Repository Diagram Style

This guide applies to SVG block diagrams, architecture diagrams, state diagrams, hardware block diagrams, and similar repository-managed illustrations.

## Goals

- Diagrams should explain structure, data flow, power flow, control paths, and risk boundaries.
- Diagrams should look consistent across one repository.
- Avoid decorative illustration. Keep engineering documents quiet and readable.

## Canvas

- Use SVG with `viewBox`.
- Common width: 1180 or 1280.
- Background: white `#ffffff`.
- Margin: 40-50.
- Prefer the same width for related diagrams.

## Text

Use a shared font declaration:

```svg
text { font-family: Consolas, "Microsoft YaHei", monospace; }
```

- Title: 18-20px, weight 700, `#1f2933`.
- Subtitle: 14px, `#5f6b75`.
- Main labels: 15px, `#1f2933`.
- Secondary labels: 13px, `#5f6b75`.
- Keep code identifiers, net names, chip names, and protocol names exact.
- Do not let text overlap lines, arrows, or module borders.

## Modules

Baseline module style:

```svg
.box { fill:#ffffff; stroke:#26313d; stroke-width:1.8; rx:7; }
```

Semantic colors:

| Meaning | Fill | Stroke |
| --- | --- | --- |
| Core logic / conversion | `#eef7ff` | `#2477b3` |
| Interface / output / normal load | `#f1faf3` | `#33824a` |
| External source / switching | `#fff8e8` | `#c27c13` |
| Power rail / high-risk power | `#fff0f0` | `#bb3b35` |
| Protection / isolation / special function | `#f8f0fb` | `#8751a1` |

Rules:

- Corner radius 6-7.
- Do not use gradients, shadows, glow, decorative dots, or background textures.
- Use inner divider lines sparingly, color `#d4dbe2`, width 1.2px.

## Lines And Arrows

| Type | Color | Width | Style |
| --- | --- | ---: | --- |
| Normal relation / bidirectional interface | `#52606d` | 2.2px | solid |
| Data / USB | `#2077b4` | 2.4px | solid |
| Power | `#c53b32` | 2.6px | solid |
| Board connector / FPC signal | `#33824a` | 2.6px | solid |
| Control | `#6b7280` | 2px | dashed `7 5` |
| Sense / detect | `#2b8a4b` | 2.1px | dashed `6 5` |

- Prefer orthogonal paths.
- Use small fixed 7x7 arrow markers.
- Set `markerUnits="userSpaceOnUse"`.
- Use white stroke around line labels instead of white rectangles.

## Agent Update Flow

1. Read this guide and the Markdown file that references the diagram.
2. Reuse existing SVG styles in the same directory if available.
3. Update diagram text and search for stale net names, chip names, and terms.
4. Verify SVG XML is parseable.
5. Verify Markdown image links exist.
6. Run `git diff --check` and inspect `git status --short`.
