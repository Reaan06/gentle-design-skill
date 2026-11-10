# Token System — the concrete library

Every value below is either captured at runtime (labeled `capture`) or taken from the
cited official documentation. Evidence log: `evidence.md`.

## 1. Semantic color roles (shadcn/ui convention — the engine v0 generates with)

Eleven roles, captured live from `ui.shadcn.com` default theme (`capture`, E1):

| Token | Default (light) | Purpose |
| --- | --- | --- |
| `--background` | white | page canvas |
| `--foreground` | near-black | primary text |
| `--card` | white | card surface (equals background — cards separate via border, not fill) |
| `--primary` | near-black (foreground-toned) | ONE action color; near-monochrome by default |
| `--primary-foreground` | white (or high-contrast ink) | Mandatory `on-brand` pair for any text/icon on `--primary` (E12) |
| `--secondary` | light gray (`lab 96.5%`) | soft action / secondary button |
| `--muted` | light gray | muted surface AND muted text (`--muted-foreground`) |
| `--accent` | light gray | hover wash |
| `--destructive` | red | destructive actions only (pair with `--destructive-foreground` / `--primary-foreground`) |
| `--border` | gray (`lab 90.95%`) | 1px structure — the primary separator, not shadows |
| `--input` | gray | control borders |
| `--ring` | mid gray | focus ring |
| `--radius` | `0.625rem` (10px) | single radius token with derived variants |

**`on-*` contrast pairing (E12)**: never pair `--primary` background with
`--foreground` text — in dark or vibrant themes they collide. Always define and apply
`--primary-foreground` (or `--on-brand`) and keep `--on-reverse` when an element must
stay dark/light across mode switches.

**`DESIGN.md` lint workaround (`@google/design.md lint`)**: Google's CLI linter parses
alpha colors (`rgba(...)`, 8-digit hex) as if composited over opaque `#FFFFFF` when
checking WCAG contrast, producing false contrast errors on dark translucent washes.
In `DESIGN.md`, declare translucent ink/wash tokens with `textColor` (never `bgColor`
+ `textColor` on an alpha swatch) or composite them to solid opaque hex approximations
specifically in the `DESIGN.md` table while keeping true alpha variables in CSS.

**Dark mode** re-maps the same roles (background → near-black, borders → low-alpha
white); components never hard-code colors. Derived variants:
`--radius-sm: calc(var(--radius) - 4px)`, `--radius-md: calc(var(--radius) - 2px)`,
`--radius-lg: var(--radius)`, `--radius-xl: calc(var(--radius) + 4px)`.

Source: ui.shadcn.com/docs/theming (verified live, E1). When a brief supplies a brand
color, map it into `--primary` (+ `--ring`), keep everything else gray.

## 2. Type scale (Tailwind v4 default ramp — what these tools generate)

Paired size/line-height from Tailwind's default text scale (tailwindcss.com/docs/font-size):

| Step | size/line-height | use |
| --- | --- | --- |
| xs | 12/16 | captions, badges |
| sm | 14/20 | secondary text, UI labels |
| base | 16/24 | body |
| lg | 18/28 | lead paragraphs |
| xl | 20/28 | emphasized body |
| 2xl | 24/32 | h4 |
| 3xl | 30/36 | h3 |
| 4xl | 36/40 | h2 |
| 5xl | 48/1 | h1 |
| 6xl–7xl | 60–72/1 | display (marketing hero) |
| 8xl–9xl | 96–128/1 | rarely; billboards only |

- Display/xl+ steps: negative letter-spacing (`-0.025em` at 5xl, up to `-0.04em`
  tighter at display) — Tailwind pairs `tracking-tight` with large steps by default.
- Captured live: v0 and Stitch hero headlines render at ~56–72px with tight tracking
  (E2). Body remains 16/24 (`capture`).
- Font stacks: system-ui stack by default (gentle-design rule); `Geist` is shadcn's
  documented default when a self-hosted font is allowed — with a true fallback stack.

## 3. Spacing rhythm (Tailwind v4: 4px base, `--spacing: 0.25rem`)

All spacing from the 4px ramp. Allowed steps (px): 1, 2, 4, 8, 12, 16, 20, 24, 32,
40, 48, 64, 80, 96, 128. Body measure ≤ `65ch`–`80ch`.

| Context | value |
| --- | --- |
| Icon↔label gap | 8 |
| Control padding (button) | 12–16 horizontal, 8–10 vertical |
| Card padding | 24 |
| Card inner gaps | 16 |
| Form field spacing | 16–20 |
| Section gap (app layouts) | 24–32 |
| Landing section vertical padding | 96–128 (`capture`: v0/Stitch hero air, E2) |
| Hero headline→subtext | 24; subtext→CTA 32 |

## 4. Radius

Single token `--radius: 0.625rem` (shadcn default; Tailwind's verified scale runs
2/4/6/8/12/16/24/32px, E7); pills/badges/avatars use `9999px`; inputs inherit
`--radius-md`. Do not mix arbitrary radii.

## 4b. Accent ramps (when a brand hue needs a scale)

Map the brand hue onto a Radix-style 12-step ramp instead of inventing tints
(radix-ui.com/colors, E7): steps 1–2 app/subtle backgrounds, 3–5 component background
rest/hover/active, 6–8 borders and focus rings, 9–10 solid rest/hover, 11–12 low/high
contrast text. Step 9 carries the highest chroma.

## 5. Elevation (shadows)

- Structure: 1px `--border`. Cards sit on the same background and separate with border.
- Real elevation only for floating layers:
  - dropdown/popover: `0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.08)`
  - modal: `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.08)`
  (Tailwind shadow-sm/shadow-2xl derivations; keep alpha ≤0.12 on light, use ring-like
  borders in dark mode instead of large shadows).

## 6. Motion

- Micro (hover/focus/toggle): 100–250ms `ease-out`; never `transition: all` (E3).
- Entrances (fade/slide/rise): 300–500ms `ease-out` (UI stays under 300ms for state
  changes, E8), staggered 40–80ms; reveals start from `scale(0.95)`, not `scale(0)`.
- Press feedback: `:active` scale ≈0.97 (E8).
- Properties: `transform`, `opacity` only; layout properties never animated.
- Always include the `prefers-reduced-motion` block disabling non-essential motion.

## 7. Texture (the professional tools' decoration vocabulary)

- Radial accent glow: one `radial-gradient` at low alpha (≤10%) behind hero.
- Dot grids / hairline grids at ~4–6% alpha for dark canvases (`capture`: Stitch
  landing, E2).
- 1px gradient hairlines (top border fade) for premium dark surfaces.
- Noise ≤3% opacity optional; never stacked decorations.
