# Pulse Analytics — token block

One system across all three artboards. The exact block below is copy-identical in
`01-landing-web.html`, `02-mobile-overview.html` and `03-desktop-workspace.html`
(verified mechanically: the three blocks are byte-equal). Each board consumes the
subset its platform needs; the token *names* never change across surfaces.

Source of the model: shadcn/ui semantic roles captured live from `ui.shadcn.com`
(evidence E1), Tailwind v4 paired type scale and `--spacing: 0.25rem` (E7), Radix
12-step ramp logic for derived alpha steps (E7), Figma Make's "~90% neutral surfaces,
brand used sparingly" (E6).

```css
:root {
  /* Semantic color roles */
  --background: #ffffff;
  --foreground: #0b1210;
  --card: #ffffff;
  --card-foreground: #0b1210;
  --popover: #ffffff;
  --popover-foreground: #0b1210;
  --primary: #0b5f4f;
  --primary-foreground: #ffffff;
  --secondary: #f3f6f5;
  --secondary-foreground: #0b1210;
  --muted: #f3f6f5;
  --muted-foreground: #596663;
  --accent: #eaf0ee;
  --accent-foreground: #0b1210;
  --destructive: #a5231b;
  --destructive-foreground: #ffffff;
  --border: #e1e6e4;
  --input: #7f8c88;
  --ring: #0b5f4f;

  /* Radius: one token + derivatives */
  --radius: 0.625rem;
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --radius-pill: 9999px;

  /* Type ramp: Tailwind v4 paired scale (E7) */
  --font-sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --text-xs: 12px;   --text-xs-lh: 16px;
  --text-sm: 14px;   --text-sm-lh: 20px;
  --text-base: 16px; --text-base-lh: 24px;
  --text-lg: 18px;   --text-lg-lh: 28px;
  --text-xl: 20px;   --text-xl-lh: 28px;
  --text-2xl: 24px;  --text-2xl-lh: 32px;
  --text-3xl: 30px;  --text-3xl-lh: 36px;
  --text-4xl: 36px;  --text-4xl-lh: 40px;
  --text-5xl: 48px;  --text-5xl-lh: 1;
  --text-6xl: 60px;  --text-6xl-lh: 1;
  --text-7xl: 72px;  --text-7xl-lh: 1;
  --tracking-display: -0.03em;
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-loose: 0.06em;
  --measure: 65ch;

  /* Spacing: 4px ramp (E7, --spacing: .25rem) */
  --space-1: 1px;    --space-2: 2px;    --space-4: 4px;    --space-8: 8px;
  --space-12: 12px;  --space-16: 16px;  --space-20: 20px;  --space-24: 24px;
  --space-28: 28px;  --space-32: 32px;  --space-36: 36px;  --space-40: 40px;
  --space-44: 44px;  --space-48: 48px;  --space-56: 56px;  --space-64: 64px;
  --space-80: 80px;  --space-96: 96px;  --space-128: 128px;

  /* Layout dimensions per platform */
  --container-max: 1216px;
  --content-max: 1120px;
  --hero-panel-w: 480px;
  --nav-h: 64px;
  --board-w: 1440px;
  --board-h: 900px;
  --frame-w: 390px;
  --frame-h: 844px;
  --safe-top: 47px;
  --safe-bottom: 34px;
  --appbar-h: 56px;
  --tabbar-h: 56px;
  --hit-min: 44px;
  --rail-w: 48px;
  --sidebar-w: 248px;
  --inspector-w: 320px;
  --topbar-h: 48px;
  --statusbar-h: 24px;
  --row-h: 32px;
  --row-tap-h: 64px;

  /* Elevation: floating layers only, alpha <= .12 */
  --shadow-popover: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.08);
  --shadow-modal: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.08);

  /* Motion */
  --duration-micro: 120ms;
  --duration-state: 180ms;
  --duration-enter: 320ms;
  --ease-out: cubic-bezier(0.2, 0.8, 0.25, 1);
  --stagger: 60ms;
}
```

## 1. Color — 5 declared colors, semantic roles only

| Role | Value | Use | Measured contrast |
| --- | --- | --- | --- |
| `--background` `--card` `--popover` | `#ffffff` | canvas, card and popover surfaces (cards separate by border, never fill) | — |
| `--foreground` | `#0b1210` | primary text, and the inverted CTA band surface | 18.95:1 on white |
| `--muted-foreground` | `#596663` | secondary text, labels, quiet iconography | 5.99:1 on white · 5.51:1 on `--secondary` · 5.19:1 on `--accent` |
| `--border` | `#e1e6e4` | 1px structure only (never text) | 1.26:1 — structural hairline, exempt (non-text) |
| `--input` | `#7f8c88` | interactive control boundary (fields, palette) | 3.49:1 on white — meets WCAG 1.4.11 |
| `--primary` (+ `--ring`) | `#0b5f4f` | the single accent: one CTA per view, active/selected indicators, data highlight | 7.60:1 on white; white on it 7.60:1 |
| `--destructive` | `#a5231b` | real error/destructive status only | 7.35:1 on white · 6.76:1 on `--secondary` |
| `--secondary` `--muted` | `#f3f6f5` | muted surface (bands, chips, table selection, status bar) | — |
| `--accent` | `#eaf0ee` | hover wash | — |

Neutral ramp (white → `--muted` → `--accent` → `--border` → `--input` →
`--muted-foreground` → `--foreground`) counts as one neutral family; with the accent
and one status red that is **3 families / 5 declared colors**, inside the 3–5 ceiling
(A5, E4) and the "~90% neutral surface" target (E6). No purple, no multi-stop brand
gradient: the only texture in the set is one masked dot grid in the web hero (E2).

## 2. Type — the documented ramp only

| Token | size/line-height | Boards that use it |
| --- | --- | --- |
| `--text-xs` | 12/16 | eyebrows (uppercase, +0.06em), table headers, captions, kbd, deltas |
| `--text-sm` | 14/20 | desktop & web UI chrome, labels, buttons, footer |
| `--text-base` | 16/24 | body copy, mobile row titles, web nav |
| `--text-lg` | 18/28 | landing hero sub-paragraph, logo row |
| `--text-xl` | 20/28 | mobile app-bar title, desktop pane title |
| `--text-2xl` | 24/32 | hero panel value, mobile KPI pair values |
| `--text-3xl` | 30/36 | *unused — declared for ramp completeness* |
| `--text-4xl` | 36/40 | section titles, mobile hero KPI value |
| `--text-5xl` | 48/1 | metrics band numbers |
| `--text-6xl` | 60/1 | *unused — declared for ramp completeness* |
| `--text-7xl` | 72/1 | landing hero display (the ceiling) |

Display steps (≥48) run `line-height: 1` with `--tracking-display: -0.03em`; section
titles use `--tracking-tight: -0.02em`; uppercase micro-labels use
`--tracking-loose: 0.06em` (B2, B6). Body measure capped by `--measure: 65ch` (B4).
Two families: `--font-sans` (system stack) and `--font-mono` (system stack) —
monospace is used for event names, key/value types and `kbd`, never for prose (A4).

## 3. Spacing — 4px ramp, nothing else

`--space-1 … --space-128` at 1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56,
64, 80, 96, 128. Values are named by their pixel size so a reviewer can check a
declaration by eye.

Deviations from the ramp list in `token-system.md` §3, with reason: **28, 36, 44, 56
are included** because `--spacing: 0.25rem` (E7) makes every 4px multiple a ramp step,
and the platform references mandate exactly these numbers — 56px app/tab bars
(`platform-mobile.md` §2), 44px minimum tap target (§3), 28–36px tree/list rows
(`platform-desktop.md` §2). Excluding them would force either an off-ramp value or an
undersized hit area; the documented list was abridged, the base scale is not.

Landing section air is `--space-96`/`--space-128` (D3); app section gaps are
`--space-12`–`--space-24`.

## 4. Radius — one token, derived

`--radius: 0.625rem` with `-sm` (−4px), `-md` (−2px), `-lg` (=), `-xl` (+4px) and
`--radius-pill: 9999px` for true pills only. Web/desktop lean on `-sm`/`-md` for
controls and `-lg`/`-xl` for surfaces; desktop deliberately never exceeds `-lg` so
chrome stays tighter than the marketing page (`platform-desktop.md` §1). No arbitrary
radius appears anywhere.

## 5. Elevation

Structure is a 1px `--border`, full stop. Only two shadows exist and both are reserved
for genuinely floating layers (alpha ≤ 0.12): `--shadow-popover` and `--shadow-modal`.
No card, pane, table row or band in the three boards casts a shadow.

## 6. Motion

`--duration-micro: 120ms` (hover/colour), `--duration-state: 180ms` (state change),
`--duration-enter: 320ms` (entrance), `--ease-out`, `--stagger: 60ms`. Only `transform`,
`opacity`, `background-color`, `color`, `border-color` and `box-shadow` are ever named
in a transition — no `transition: all` (E3). Press feedback is `scale(0.97)` (E8).
Each file ends with a `prefers-reduced-motion: reduce` block that flattens durations.

## 7. Layout dimension tokens

Platform dimensions live in `:root` too, so no raw px appears in component CSS:

`--board-w/h: 1440/900` (web + desktop viewport) · `--frame-w/h: 390/844` (mobile) ·
`--nav-h: 64` · `--container-max: 1216` · `--content-max: 1120` ·
`--hero-panel-w: 480` · `--safe-top: 47` `--safe-bottom: 34` ·
`--appbar-h: 56` `--tabbar-h: 56` `--hit-min: 44` · `--rail-w: 48` ·
`--sidebar-w: 248` `--inspector-w: 320` `--topbar-h: 48` `--statusbar-h: 24` ·
`--row-h: 32` `--row-tap-h: 64`.

## 7b. Platform notes tied to the block

- **Mobile (`02`)** uses the **iOS-like** type system named in the artboard comment and
  manifest tradeoff: body 16/24 minimum, labels 12 minimum, and the iOS/M3 22px title
  step **collapsed onto the ramp's 20/28 step** (`--text-xl`) rather than shipping an
  off-ramp 22px — the ramp wins over the platform list's isolated number (E7) and the
  hierarchy is unchanged because weight and spacing carry it.
- **Desktop (`03`)** uses `--text-sm` (14) for all chrome, `--row-h` (32) for table rows
  and `--space-28` (28) for tree rows; panel radius never exceeds `--radius-lg`. Light
  theme is the deliberate choice for a BI surface (see the board's manifest tradeoff);
  the same block re-maps to dark without touching component CSS.
- **Web (`01`)** is the only board that consumes `--text-5xl`, `--text-7xl`,
  `--hero-panel-w` and the 96/128 section air.

## 8. What may appear outside `:root`

Only three literal values are allowed in component CSS, and each is structural rather
than a design decision: `1px` (hairline borders, exactly as shadcn emits
`1px solid var(--border)` — E1), `2px` (the mandated focus ring: `outline: 2px solid
var(--ring); outline-offset: 2px`), and `0`. Everything else resolves through a
`var()` or a `calc()`/`color-mix()` derivation of a token. Data geometry (bar heights,
heatmap alpha, meter fill) is passed as a `--v`/`--a` custom property from the markup,
so "the property is styled, the value is data".

## 9. Dark re-map (S12)

`04-mobile-dark.html` and `05-desktop-dark.html` carry **the same token names** with
dark values. Sections 1–8 above describe the light block and are
unchanged; this section is the dark half of the same system. Mapping rules, contrast
method, elevation model and the 10-item dark checklist live in
`skill/gentle-design-skill/references/dark-mode.md`.

```css
:root {                                  /* the dark half of the block */
  color-scheme: dark;
  --background: #0c100f;                 /* oklch .168 .007 179 */
  --foreground: #e9efed;                 /* oklch .947 — not pure white */
  --card: #1c2221;
  --card-foreground: #e9efed;
  --popover: #232a29;
  --popover-foreground: #e9efed;
  --primary: #5fd6b8;
  --primary-foreground: #05100d;
  --secondary: rgb(255 255 255 / 0.06);
  --secondary-foreground: #e9efed;
  --muted: rgb(255 255 255 / 0.06);
  --muted-foreground: #9daba7;
  --accent: rgb(255 255 255 / 0.08);
  --accent-foreground: #e9efed;
  --destructive: #f4786a;
  --destructive-foreground: #170604;
  --border: rgb(255 255 255 / 0.12);
  --input: rgb(255 255 255 / 0.38);
  --ring: #8be8d2;
  --shadow-popover: 0 4px 6px -1px rgb(0 0 0 / 0.5), 0 0 0 1px rgb(255 255 255 / 0.1);
  --shadow-modal: 0 20px 25px -5px rgb(0 0 0 / 0.6), 0 0 0 1px rgb(255 255 255 / 0.1);
}
```

### 9.1 Dark value per token

| Token | Light | Dark | Measured on the dark pairs |
| --- | --- | --- | --- |
| `--background` | `#ffffff` | `#0c100f` (oklch L .168, C .007) | canvas; near-black, low chroma, accent hue |
| `--foreground` | `#0b1210` | `#e9efed` (L .947) | 16.44:1 on background · 13.87:1 on card · 12.57:1 on popover |
| `--card` | `#ffffff` | `#1c2221` (L .246) | elevation step +0.078 L over background |
| `--card-foreground` | `#0b1210` | `#e9efed` | same as `--foreground` |
| `--popover` | `#ffffff` | `#232a29` (L .278) | top of the surface ladder |
| `--popover-foreground` | `#0b1210` | `#e9efed` | same as `--foreground` |
| `--primary` | `#0b5f4f` | `#5fd6b8` (L .800) | 10.76:1 on background · 9.07:1 on card |
| `--primary-foreground` | `#ffffff` | `#05100d` (L .160) | 10.86:1 on `--primary` |
| `--secondary` | `#f3f6f5` | `rgb(255 255 255 / 0.06)` | composites to `#1b1e1d` on canvas (L .231), `#2a2f2e` on card (L .300) |
| `--secondary-foreground` | `#0b1210` | `#e9efed` | 14.43:1 on the secondary composite |
| `--muted` | `#f3f6f5` | `rgb(255 255 255 / 0.06)` | same value as `--secondary`, as in light |
| `--muted-foreground` | `#596663` | `#9daba7` (L .729) | 8.04:1 background · 6.78:1 card · 6.15:1 popover · 5.71:1 on a wash over card |
| `--accent` | `#eaf0ee` | `rgb(255 255 255 / 0.08)` | hover wash; `#1f2322` on canvas, `#2e3433` on card |
| `--accent-foreground` | `#0b1210` | `#e9efed` | 13.64:1 on the accent composite over canvas |
| `--destructive` | `#a5231b` | `#f4786a` (L .714) | 7.06:1 background · 5.95:1 card · 6.45:1 on its own 8% wash |
| `--destructive-foreground` | `#ffffff` | `#170604` | 7.27:1 on `--destructive` (white would be 2.33:1) |
| `--border` | `#e1e6e4` | `rgb(255 255 255 / 0.12)` | 1.37:1 vs canvas — structural hairline, exempt; matches light's 1.26:1 |
| `--input` | `#7f8c88` | `rgb(255 255 255 / 0.38)` | 3.56:1 canvas · 3.51:1 card · 3.41:1 popover · 3.12:1 on a wash — WCAG 1.4.11 ≥3:1 |
| `--ring` | `#0b5f4f` | `#8be8d2` (L .867) | 13.29:1 canvas · 11.21:1 card (2px outline, offset 2px, verified in the render) |
| `--shadow-popover` / `--shadow-modal` | black alpha ≤0.12 | black alpha 0.5 / 0.6 **+ `0 0 0 1px rgb(255 255 255 / 0.1)` ring** | light alphas are invisible on near-black |
| `--radius*`, type ramp, spacing ramp, motion (`--duration-*`, `--ease-out`, `--stagger`) | — | **unchanged** | only color roles flip |

### 9.2 Notes that make the table checkable

1. **Elevation is the L ladder, not shadow.** `0.168 → 0.246 → 0.278`. The order is load
   bearing: `--secondary` over canvas (L .231) must stay **below** `--card` (L .246) or
   the pressed segment chip in `03`/`05` reads sunken. That is why `--card` is lighter
   than a naive shadcn-dark card; the component was not touched.
2. **Alpha tokens have no contrast on their own.** All ratios above are computed on the
   *composited* value (white α over the parent surface), which is what renders; the
   browser audit reads computed colors and composites the ancestor stack, so the numbers
   are reproducible from the render, not only from this file.
3. **`--input` is intentionally louder than `--border`.** 38% white vs 12% white: control
   boundaries owe 1.4.11's 3:1, hairlines owe nothing. Same asymmetry as light
   (`#7f8c88` 3.49:1 vs `#e1e6e4` 1.26:1). The one text using `--input` in `05` is the
   breadcrumb `/` separator, which is `aria-hidden` decoration between links.
4. **Primary inverts as a light pill** (`#5fd6b8` + `#05100d` text, 10.86:1), the strategy
   named in `dark-mode.md` §2.5(a). Reusing the light `#0b5f4f` would be 1.9:1.
5. **No pure white on black.** `--foreground` sits at L .947 over a canvas at L .168.
6. **Static preview pins dark** (`:root` + `data-theme="dark"` + `color-scheme: dark`), so
   the screenshot does not depend on the viewer's OS. The runtime rule is the same
   declaration set under `@media (prefers-color-scheme: dark)`; no JS owns the theme
   (`dark-mode.md` §6).
7. **Texture**: the two dark boards are texture-free (no glows, no dot grids) — the only
   textured board remains the light web landing. If `01` ever gets a dark variant, its
   dot grid halves from 6% to ~3%.
8. **Verification** (`agent-browser`, `file://`, 390×844 and 1440×900): zero element
   overflow, geometry and DOM shape byte-identical to `02`/`03`, every text pair ≥5.7:1
   except the `aria-hidden` separator (3.56:1, non-text per 1.4.3), focus-visible ring
   renders `rgb(139,232,210)` 2px/offset 2px, and `prefers-reduced-motion: reduce`
   flattens animations to 1ms.
