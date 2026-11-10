---
version: alpha
name: Pulse Analytics
description: "Near-monochrome product-analytics design system: one deep-teal accent, 1px borders instead of shadows, the documented Tailwind type ramp, a 4px spacing ramp, and one token set with light and dark value maps."
---

# Pulse Analytics — Design System

This file is the system of record for the five Pulse artboards in this folder
(`01-landing-web.html`, `02-mobile-overview.html`, `03-desktop-workspace.html`,
`04-mobile-dark.html`, `05-desktop-dark.html`). The YAML token blocks are normative;
the prose explains why the values are what they are. Values are copied from
`tokens.md`, which is mechanically identical to the `:root` block that all three light
boards share byte for byte.

## Overview

**Brand & style.** Pulse is a product-analytics SaaS for teams that ship weekly. The
interface is an instrument, not a poster: it is judged by how quickly a number can be
trusted, not by how impressive the first viewport looks. The voice is quiet and
accountable — dense layouts, full-strength text, no decoration that competes with data.

- **Personality:** precise, calm, technical. The confidence of a measuring device.
- **Audience:** product managers, growth analysts and data engineers who keep the
  workspace open for hours. They read tables, not hero sections — except once, on the
  marketing page.
- **Emotional response:** "this will not lie to me." Delight is deliberately absent
  from data surfaces; motion exists only to explain a state change.
- **Non-goals:** showcase gradients, glass panels, soft 3D blobs, illustration
  mascots, gradient text, dark-by-default marketing pages. None appear; the only
  texture in the whole system is one masked dot grid on the web hero.

**The three commitments.**

1. **Near-monochrome plus one accent.** ~90% of every surface is neutral; the single
   saturated role is Harbor Teal in `primary` and `ring`. There is no second accent,
   no multi-stop brand gradient, no purple.
2. **Structure is a 1px line, not a shadow.** Cards, panes, bands, rows and the
   palette all separate with a hairline border on the same surface. Shadows are
   reserved for genuinely floating layers.
3. **Everything is provable.** Contrast ratios in this document are measured from the
   token values (WCAG 2.1 relative luminance), not asserted. Layout, radius, type and
   spacing all resolve through the ramps; three literals are allowed outside the
   token block and each is structural (`1px`, `2px`, `0`).

**Substitution test (passed).** Replace the wordmark, hero copy and accent hue and see
whether the page is still plausibly another company's template. Pulse survives because
three decisions only fit a measurement product: a left-aligned 72px display over a real
funnel panel with data geometry instead of an illustration; a full-bleed *inverted*
metrics band (foreground surface, white numerals) where a template would put a
three-card feature grid; and a quiet single-line logo row instead of proof-by-logo
walls. The remaining structure — split feature, four-column footer, single CTA — is
deliberately conventional so that the product-specific decisions carry the identity.

## Colors

Three color families — one neutral ramp (Paper White → Fog Wash → Mist → Hairline
Gray → Control Gray → Slate Sage → Graphite Ink), one accent (Harbor Teal) and one
status red (Clay Red) — inside the 3–5 family ceiling and inside the "~90% neutral
surface" target. There is no purple, no second accent and no multi-stop brand
gradient anywhere in the system.

- **Graphite Ink (#0b1210):** `foreground`. All body and headline text. 18.95:1 on
  Paper White — the system never trades text contrast for softness.
- **Paper White (#ffffff):** `background`, `card`, `popover`. Cards do **not** get a
  different fill from the page; they separate by border, per the card-necessity rule.
- **Harbor Teal (#0b5f4f):** `primary` and `ring`. One action per view, active and
  selected indicators, data highlight, focus ring. 7.60:1 on Paper White and the same
  ratio for white on it, so it is legal as a filled button and as text.
- **Fog Wash (#f3f6f5):** `secondary` and `muted`. Muted surfaces, bands, chips,
  selected rows, status bar. Text on it: Slate Sage 5.51:1, Ink 17.5:1.
- **Mist (#eaf0ee):** `accent`. Hover wash only, never a resting surface. 5.19:1 for
  Slate Sage, 16.5:1 for Ink.
- **Hairline Gray (#e1e6e4):** `border`. Structure only, never text — 1.26:1 is
  intentional, because a separator that measured 4.5:1 would read as a divider of
  content rather than a boundary of layout.
- **Control Gray (#7f8c88):** `input`. Interactive control boundaries at 3.49:1,
  which clears WCAG 1.4.11's 3:1 for non-text UI. Intentionally louder than
  `border`: boundaries owe contrast, hairlines do not.
- **Slate Sage (#596663):** `muted-foreground`. Labels, captions, secondary text.
- **Clay Red (#a5231b):** `destructive`. Real error and destructive status only —
  never a decorative highlight. 7.35:1 on Paper White, 6.76:1 on Fog Wash.

Measured text pairs, all above the 4.5:1 floor:

| Pair | Ratio |
| --- | --- |
| `foreground` on `background` / `card` / `popover` | 18.95:1 |
| `muted-foreground` on `background` | 5.99:1 |
| `muted-foreground` on `secondary` | 5.51:1 |
| `muted-foreground` on `accent` | 5.19:1 |
| `primary` on `background` · `primary-foreground` on `primary` | 7.60:1 |
| `destructive` on `background` | 7.35:1 |
| `destructive` on `secondary` | 6.76:1 |
| `foreground` on `secondary` | 17.48:1 |
| `accent-foreground` on `accent` | 16.48:1 |

### Dark re-map

Dark is not a second design system: it is the same nineteen role names with different
values, so no component CSS changes. Only color roles flip; radius, type, spacing,
motion and dimensions are identical. From `dark-mode.md`:

- **Elevation is lightness, not shadow.** The surface ladder is
  `background` L 0.168 → `card` L 0.246 → `popover` L 0.278. The order is load bearing:
  a 6% wash over the canvas (L 0.231) must stay *below* `card`, or a pressed segment
  chip reads sunken.
- **No pure white on black.** `foreground` sits at L 0.947 (#e9efed) over a L 0.168
  canvas; 16.44:1 is already more contrast than the eye needs.
- **Hairlines become low-alpha white.** `border` is 12% white (1.37:1, structural) and
  `input` is 38% white (3.56:1, WCAG 1.4.11) — the same asymmetry as light.
- **`primary` inverts into a light pill** (#5fd6b8 with #05100d text, 10.86:1).
  Reusing the light teal would be 1.9:1 on the dark canvas.
- **`ring` lightens independently** (#8be8d2, 13.29:1) so the 2px focus outline stays
  the loudest element on the screen.
- **Alpha washes are not colors on their own.** All measured ratios for `secondary`,
  `muted`, `accent`, `border` and `input` are computed on the composited value (white
  α over the parent surface), which is what renders.
- **Theme ownership:** the runtime rule is a `prefers-color-scheme: dark` media query
  with the same declarations; the static boards pin `data-theme="dark"` plus
  `color-scheme: dark` so a screenshot never depends on the viewer's OS. No JavaScript
  owns the theme.

### Design Tokens

```yaml
colors:
  # Light — the eleven shadcn-style semantic roles, plus popover and status
  background: "#ffffff"
  foreground: "#0b1210"
  card: "#ffffff"
  card-foreground: "#0b1210"
  popover: "#ffffff"
  popover-foreground: "#0b1210"
  primary: "#0b5f4f"
  primary-foreground: "#ffffff"
  secondary: "#f3f6f5"
  secondary-foreground: "#0b1210"
  muted: "#f3f6f5"
  muted-foreground: "#596663"
  accent: "#eaf0ee"
  accent-foreground: "#0b1210"
  destructive: "#a5231b"
  destructive-foreground: "#ffffff"
  border: "#e1e6e4"
  input: "#7f8c88"
  ring: "#0b5f4f"

  # Dark — the same roles re-mapped (oklch chroma stays under .02 except on primary)
  background-dark: "#0c100f"
  foreground-dark: "#e9efed"
  card-dark: "#1c2221"
  card-foreground-dark: "#e9efed"
  popover-dark: "#232a29"
  popover-foreground-dark: "#e9efed"
  primary-dark: "#5fd6b8"
  primary-foreground-dark: "#05100d"
  secondary-dark: "rgb(255 255 255 / 0.06)"
  secondary-foreground-dark: "#e9efed"
  muted-dark: "rgb(255 255 255 / 0.06)"
  muted-foreground-dark: "#9daba7"
  accent-dark: "rgb(255 255 255 / 0.08)"
  accent-foreground-dark: "#e9efed"
  destructive-dark: "#f4786a"
  destructive-foreground-dark: "#170604"
  border-dark: "rgb(255 255 255 / 0.12)"
  input-dark: "rgb(255 255 255 / 0.38)"
  ring-dark: "#8be8d2"
```

## Typography

The ramp is Tailwind v4's paired size/line-height scale — the same ramp these tools
generate by default — carried over unchanged: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60,
72 px with their paired line heights. Nothing off-ramp appears. Two families, both
system stacks: `ui-sans-serif` with a real fallback chain for UI and prose, and
`ui-monospace` for event names, key/value types and `kbd` chips only — never for prose,
never for headings. Nothing is loaded over the network, so there is no FOUT and no font
license surface.

- **Display (48–72px):** line height `1`, tracking `-0.03em`. The web hero sets 72px at
  a 12ch measure so the line breaks are part of the composition rather than left to
  `text-wrap: balance` alone.
- **Headlines (24–36px):** `-0.02em` tracking; weight 600 carries hierarchy without a
  size jump.
- **Body:** 16/24 default, 18/28 for lead paragraphs, 14/20 for app chrome. The measure
  is capped at 65ch on marketing prose.
- **Labels:** 14/20 medium for buttons and controls; 12/16 medium for eyebrows, table
  headers, badges and `kbd`, uppercase with `+0.06em` tracking.
- **Weights:** three only — 400, 500, 600. Nothing above 600 exists in the system, so
  emphasis can never be faked by weight escalation.
- **One mono role:** `code-sm` (12/16, regular) is the only monospace token — event
  names, key/value types and `kbd` chips. Monospace never sets prose or headings.
- **Declared but unused:** `display-xl` (60/1) and `headline-md` (30/36) are part of
  the ramp but no artboard consumes them; they exist so a missing step never tempts an
  off-ramp value. The mobile 22px title step (iOS/M3) collapses onto `title-md` (20/28)
  rather than shipping an off-ramp size — hierarchy is carried by weight and spacing.
- **Numerals:** tabular figures (`font-variant-numeric: tabular-nums`) are applied per
  numeric cell in the desktop table, not to a whole type role.

### Design Tokens

```yaml
typography:
  display-2xl:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 72px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: -0.03em
  display-xl:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 60px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: -0.03em
  display-lg:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 36px
    fontWeight: 600
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 30px
    fontWeight: 600
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-sm:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 24px
    fontWeight: 600
    lineHeight: 32px
    letterSpacing: -0.02em
  title-md:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 20px
    fontWeight: 600
    lineHeight: 28px
    letterSpacing: -0.02em
  body-lg:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 18px
    fontWeight: 400
    lineHeight: 28px
    letterSpacing: 0em
  body-md:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 16px
    fontWeight: 400
    lineHeight: 24px
    letterSpacing: 0em
  body-sm:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
    letterSpacing: 0em
  label-md:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 14px
    fontWeight: 500
    lineHeight: 20px
    letterSpacing: 0em
  label-sm:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    fontSize: 12px
    fontWeight: 500
    lineHeight: 16px
    letterSpacing: 0.06em
  code-sm:
    fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'
    fontSize: 12px
    fontWeight: 400
    lineHeight: 16px
    letterSpacing: 0em
```

## Layout

A 4px base scale (`--spacing: 0.25rem`). Every step is named by its pixel value so a
reviewer can validate a declaration by eye, and every 4px multiple is a legal step: 1,
2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 80, 96, 128. The abridged
list in the token library omits 28, 36, 44 and 56; they are included here because the
platform references require 56px app and tab bars, a 44px minimum tap target and
28–36px desktop list rows — excluding them would force either an off-ramp value or an
undersized hit area.

- **Air:** marketing sections run 96–128px vertically; app surfaces (mobile and
  desktop) run 12–24px section gaps. The difference is deliberate: one page is read
  once, the other is read all day.
- **Containers:** 1216px page container, 1120px content column, 480px hero product
  panel. Desktop layout is a fixed 48px activity rail, a 248px tree, a fluid table
  region and a 320px inspector, under a 48px top bar and above a 24px status bar.
- **Density:** 32px desktop table rows, 28px tree rows and table header, 20px badges,
  24px segmented items, 32px controls. Mobile keeps 64px tap rows, 56px app and tab
  bars, 47px top and 34px bottom safe areas, and a 44px minimum hit target.
- **Measure:** prose is capped at 65ch; the hero display is capped at 12ch. No layout
  relies on text alone for alignment — numeric columns are right-aligned and use
  tabular figures.

### Design Tokens

```yaml
spacing:
  space-1: 1px
  space-2: 2px
  space-4: 4px
  space-8: 8px
  space-12: 12px
  space-16: 16px
  space-20: 20px
  space-24: 24px
  space-28: 28px
  space-32: 32px
  space-36: 36px
  space-40: 40px
  space-44: 44px
  space-48: 48px
  space-56: 56px
  space-64: 64px
  space-80: 80px
  space-96: 96px
  space-128: 128px
  gutter: 24px
  card-padding: 24px
  section-web: 128px
  section-app: 24px
  row-height: 32px
  hit-min: 44px
  container-max: 1216px
  content-max: 1120px
  board-width: 1440px
  frame-width: 390px
  measure: 65ch
```

## Elevation & Depth

Depth is **borders and lightness**, not shadow. `card` equals `background` in light
mode precisely so a card cannot be faked with a fill: a card is a 1px `border` plus
padding. The hierarchy order the system commits to is: alignment → font weight → 1px
border → tonal wash (`secondary` / `accent`) → color (`primary`) → shadow. Shadow is
last, and almost never reached.

- **Exactly two shadow tokens exist**, both for floating layers only and both at alpha
  ≤ 0.12: `--shadow-popover` (`0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.08)`)
  and `--shadow-modal`
  (`0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.08)`).
- **No card, pane, band, table row or chip casts a shadow.** The two floating-layer
  tokens are declared for popovers and modals; no artboard exercises either. Every
  `box-shadow` that does appear in the boards is really a border — `inset 0 0 0 1px
  var(--border)` on a selected segment or a skeleton cell — or a surface-coloured
  2px halo (`0 0 0 2px var(--background)`) on a mobile avatar.
- **Pressed-state "depth" is a border, not a shadow.** A selected segment chip is
  `card` on the wash track with `inset 0 0 0 1px border`; a selected table row is a
  `secondary` fill with a 2px `primary` inset bar on the left edge.
- **Dark mode replaces shadow with the lightness ladder** (L 0.168 → 0.246 → 0.278)
  and, on floating layers only, a 1px white ring at 10% — the same information a light
  shadow carries, expressed as an edge. Large dark shadows would read as smudge.
- **Texture is capped at one element per view.** The web hero carries a single dot
  grid — 1px `border` dots on a 24px grid at 0.55 element opacity (≈6% effective alpha),
  masked to a radial ellipse over the right shoulder of the hero. The dark boards carry
  none. No glow, no noise, no stacked gradient meshes.

## Shapes

One radius token, `10px` (`--radius: 0.625rem`), with three derived steps and one
pill. Every corner in every board resolves through that single decision, so radius
never becomes a second, accidental visual language.

- `sm` 6px — controls inside a container (segment items, table literals, checkbox).
- `md` 8px — the default interactive radius: buttons, inputs, segmented tracks,
  palette.
- `lg` 10px — surfaces: cards, panes, inspector.
- `xl` 14px — the marketing hero panel only. Desktop chrome deliberately never
  exceeds `lg`, so app furniture stays tighter than the landing page.
- `full` 9999px — true pills only: badges, avatars, status dots. A pill on a
  rectangular control is a bug, and mixing radii inside one view is a bug.

### Design Tokens

```yaml
rounded:
  sm: 6px
  md: 8px
  lg: 10px
  xl: 14px
  full: 9999px
```

## Components

Components are defined by their states, not their resting look. Every interactive atom
carries the full four-state matrix — hover, `:focus-visible`, `:active`, `:disabled` —
and `:focus-visible` is the one state that is never suppressed (`outline: 2px solid
var(--ring); outline-offset: 2px`, 2px + 2px offset).

- **Buttons.** 40px default (48px `lg` on the marketing hero, 32px `sm` in dense
  desktop chrome), 16px inline padding (24 / 12 at the size extremes), radius `md`,
  `label-md`. `primary` is Harbor Teal and filled; `ghost` is transparent with a 1px
  `border` and `foreground` text; `inverse` is Paper White on the inverted band.
  Hover darkens `primary` by mixing 86% primary with 14% foreground — never by lowering
  opacity, which would drop text contrast. `:active` is `scale(0.97)`; `:disabled` is
  opacity 0.45 with `cursor: not-allowed`. One primary action per view.
- **Segmented control.** 24px `secondary` track with a 1px `border`, radius `md`;
  items are 24px tall, radius `sm`, `label-sm`, `muted-foreground` at rest, `foreground`
  on hover (`accent` wash) and `foreground` on `card` when `aria-pressed="true"`.
- **Badges.** 20px pills, 8px inline padding, `label-sm`. Muted badges are `secondary`
  with `muted-foreground` text (5.51:1). Alert badges are a *tinted* status surface —
  8% Clay Red over `background` with `destructive` text, at or above the 6.76:1
  measured for `destructive` on `secondary` — so a status never becomes a solid block
  of red in a dense table. Badges never carry an action.
- **Destructive.** The filled danger affordance is `destructive` with
  `destructive-foreground` (7.35:1 light, 7.27:1 dark), 32px tall, radius `md`. No
  artboard shows one; the pair is declared so a future confirmation step cannot invent
  its own red.
- **Fields.** No artboard contains a native text input. The control that carries the
  `input` boundary is the 32px command-palette trigger: `card` fill,
  `muted-foreground` text (5.99:1 light, 6.78:1 on a dark card), radius `md`, and
  `1px solid input` (3.49:1 light, 3.56:1 dark — a field boundary always owes 3:1,
  unlike a hairline). Any future field inherits that geometry, and its boundary is
  `input`, never `border`.
- **Lists and rows.** 32px desktop rows separated by a 50%-border hairline, 64px
  mobile tap rows, hover wash `accent`, pressed `secondary`, selected `secondary` plus
  a 2px `primary` inset edge. Tree rows are 28px; table headers 28px, sticky, with
  `aria-sort` state.
- **Tooltips.** The activity rail's icon buttons render one from
  `content: attr(data-tip)`: surface inverts (`foreground` fill, `background` text),
  radius `sm`, `label-sm`, 4px/8px padding, offset 4px from the rail, revealed by an
  opacity transition with a 300ms delay. Text only, never an action. The `popover`
  role stays declared for floating menus, which no artboard exercises. The breadcrumb
  `/` separator is `input` coloured and `aria-hidden` — decoration between links, not
  body copy.
- **Motion.** Micro 120ms, state change 180ms, entrance 320ms, `ease-out`
  (`cubic-bezier(0.2, 0.8, 0.25, 1)`), stagger 60ms. Only `transform`, `opacity`,
  `background-color`, `color`, `border-color` and `box-shadow` are ever transitioned —
  no `transition: all`, no animated layout properties. A `prefers-reduced-motion:
  reduce` block flattens durations at the end of every board.
- **Declared roles.** `card-foreground`, `popover-foreground`, `secondary-foreground`,
  `accent-foreground` and `destructive-foreground` are declared roles: the boards reach
  for `foreground` where the values are identical, while this document states the
  intent (text on a card uses `card-foreground`, not `foreground`). `popover` and
  `muted` are surfaces the artboards only meet through their `card`/`secondary`
  equivalents. The dark wash/dark text pairs are recorded separately
  (`text-on-hover-dark`) because the CLI can score text only against an opaque
  background, while the real hover wash is 8% white over `card` (13.64:1 composited).

### Design Tokens

```yaml
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
  card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    rounded: "{rounded.lg}"
    padding: 24px
    typography: "{typography.body-md}"
  popover:
    backgroundColor: "{colors.popover}"
    textColor: "{colors.popover-foreground}"
    rounded: "{rounded.lg}"
    padding: 12px
    width: 240px
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    padding: 16px
    height: 40px
    typography: "{typography.label-md}"
  button-primary-lg:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    padding: 24px
    height: 48px
    typography: "{typography.body-md}"
  button-primary-sm:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 32px
    typography: "{typography.label-md}"
  button-ghost:
    textColor: "{colors.foreground}"
    rounded: "{rounded.md}"
    padding: 16px
    height: 40px
    typography: "{typography.label-md}"
  palette-trigger:
    backgroundColor: "{colors.card}"
    textColor: "{colors.muted-foreground}"
    rounded: "{rounded.md}"
    height: 32px
    padding: 12px
    typography: "{typography.body-sm}"
  field-boundary:
    backgroundColor: "{colors.input}"
    height: 1px
  focus-ring:
    backgroundColor: "{colors.ring}"
    size: 2px
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
  segmented-control:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.md}"
    height: 24px
    padding: 2px
    typography: "{typography.label-sm}"
  segmented-control-item:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.sm}"
    typography: "{typography.label-sm}"
  badge:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.muted-foreground}"
    rounded: "{rounded.full}"
    height: 20px
    padding: 8px
    typography: "{typography.label-sm}"
  button-destructive:
    backgroundColor: "{colors.destructive}"
    textColor: "{colors.destructive-foreground}"
    rounded: "{rounded.md}"
    height: 32px
    padding: 12px
    typography: "{typography.label-md}"
  menu-item-hover:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-foreground}"
    rounded: "{rounded.sm}"
    height: 32px
    padding: 12px
    typography: "{typography.body-sm}"
  table-header:
    backgroundColor: "{colors.background}"
    textColor: "{colors.muted-foreground}"
    height: 28px
    typography: "{typography.label-sm}"
  table-row-selected:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.foreground}"
    height: 32px
    typography: "{typography.body-sm}"
  event-name:
    textColor: "{colors.foreground}"
    typography: "{typography.code-sm}"

  page-dark:
    backgroundColor: "{colors.background-dark}"
    textColor: "{colors.foreground-dark}"
  card-dark:
    backgroundColor: "{colors.card-dark}"
    textColor: "{colors.card-foreground-dark}"
    rounded: "{rounded.lg}"
    padding: 24px
    typography: "{typography.body-md}"
  popover-dark:
    backgroundColor: "{colors.popover-dark}"
    textColor: "{colors.popover-foreground-dark}"
    rounded: "{rounded.lg}"
    padding: 12px
    width: 240px
  button-primary-dark:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.primary-foreground-dark}"
    rounded: "{rounded.md}"
    padding: 16px
    height: 40px
    typography: "{typography.label-md}"
  button-primary-sm-dark:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.primary-foreground-dark}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 32px
    typography: "{typography.label-md}"
  palette-trigger-dark:
    backgroundColor: "{colors.card-dark}"
    textColor: "{colors.muted-foreground-dark}"
    rounded: "{rounded.md}"
    height: 32px
    padding: 12px
    typography: "{typography.body-sm}"
  field-boundary-dark:
    backgroundColor: "{colors.input-dark}"
    height: 1px
  focus-ring-dark:
    backgroundColor: "{colors.ring-dark}"
    size: 2px
  divider-dark:
    backgroundColor: "{colors.border-dark}"
    height: 1px
  segmented-control-dark:
    backgroundColor: "{colors.secondary-dark}"
    rounded: "{rounded.md}"
    height: 24px
    padding: 2px
  segmented-control-item-dark:
    backgroundColor: "{colors.card-dark}"
    textColor: "{colors.secondary-foreground-dark}"
    rounded: "{rounded.sm}"
    typography: "{typography.label-sm}"
  badge-dark:
    backgroundColor: "{colors.muted-dark}"
    rounded: "{rounded.full}"
    height: 20px
    padding: 8px
  button-destructive-dark:
    backgroundColor: "{colors.destructive-dark}"
    textColor: "{colors.destructive-foreground-dark}"
    rounded: "{rounded.md}"
    height: 32px
    padding: 12px
    typography: "{typography.label-md}"
  menu-item-hover-dark:
    backgroundColor: "{colors.accent-dark}"
    rounded: "{rounded.sm}"
    height: 32px
    padding: 12px
  text-on-hover-dark:
    textColor: "{colors.accent-foreground-dark}"
    typography: "{typography.body-sm}"
  table-header-dark:
    backgroundColor: "{colors.background-dark}"
    textColor: "{colors.muted-foreground-dark}"
    height: 28px
    typography: "{typography.label-sm}"
  event-name-dark:
    textColor: "{colors.foreground-dark}"
    typography: "{typography.code-sm}"
```

## Do's and Don'ts

- Do use `primary` for the single most important action per view — one filled teal
  button in a viewport, not one per section. Region-scoped primaries are allowed only
  in the desktop workspace (toolbar, empty state), never two in the same region.
- Do separate surfaces with a 1px `border`. Don't add a shadow to anything that is not
  a popover or a modal; the system has exactly two shadow tokens and both are reserved,
  not spent.
- Do spend hierarchy in this order: alignment, weight, border, wash, accent, shadow.
- Do keep at least 4.5:1 for every text pair. `border` (1.26:1 light / 1.37:1 dark) is
  a structural hairline and must never carry text; `input` owes 3:1 as a control
  boundary only.
- Do express hover on `primary` as a color mix (86% primary + foreground). Don't fake
  states with opacity — a `:disabled` opacity of 0.40–0.45 is the only legal opacity
  change on an interactive element, and it is never used to make text "quieter".
- Do transition only `transform`, `opacity`, `background-color`, `color`,
  `border-color` and `box-shadow`, in 120–320ms `ease-out`. Never `transition: all`,
  never an animated width, height, top or left.
- Do keep press feedback at `scale(0.97)` and preserve a 2px focus ring with 2px
  offset on every interactive element, in both themes.
- Do use the documented type ramp only. Don't invent a 22px or 13px step; collapse a
  platform-specific size onto the nearest ramp step and carry the difference in weight
  or spacing.
- Do use one radius per element and never exceed `lg` (10px) in app chrome; `xl` (14px)
  belongs to the marketing hero panel alone. Don't mix pill and rectangular radii in
  one view.
- Do keep spacing on the 4px ramp, named by pixel value. Don't nudge a gap by 3px to
  make something fit.
- Do keep dark mode a value re-map only: same role names, same component CSS, surfaces
  ordered by lightness (background → card → popover) with low-alpha white hairlines.
  Don't ship pure white text on pure black, and don't reuse the light teal as a dark
  filled button.
- Do keep decoration to one element per view (the web hero's masked dot grid at ~6%
  alpha). Don't stack a glow, a grid and noise, and never put a glow behind data.
- Do respect the substitution test before adding a section: if the new block would
  read identically with another company's wordmark, it is template furniture — replace
  it with something that only fits a measurement product.
- Don't introduce a second accent, a multi-stop gradient, glassmorphism, or an emoji
  used as an icon. The system has one hue and a status red, and that is the budget.
- Don't use dashed or decorative borders, gradient text, or centered hero copy at
  display size — the hero is left-aligned by design.
