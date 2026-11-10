---
version: alpha
name: Molino
description: "Editorial print design system for an Argentine neighbourhood coffee roastery: warm paper #FAF7F2, printing ink #1A1815, one oxblood #7F1D1D spent at most three times per view, 1px ink rules instead of shadows, a near-straight 2px radius, and a serif page with a grotesque label voice."
---

# Molino — Design System

This file is the system of record for the two Molino artboards in this folder
(`01-tienda.html`, `02-suscripcion.html`). The YAML token blocks are normative; the
prose explains why the values are what they are. Every value is copied from
`tokens.md`, which is mechanically identical to the `:root` block that both boards
share byte for byte.

## Overview

**Brand & style.** Molino is a neighbourhood coffee roastery in Colegiales, Buenos
Aires: eighteen kilos roasted every Tuesday, delivered every Thursday, one printed
label per lot. The site is a magazine that also sells the coffee. It is not a
marketplace with a hero image; it is a printed page where the product *is* its label.

- **Personality:** quiet, warm, precise. A shop that writes down the altitude.
- **Audience:** home brewers in Buenos Aires who already own a scale and a grinder and
  who can taste the difference between a washed Chiapas and a natural Yirgacheffe.
- **Emotional response:** "this arrives on Thursday, and someone roasted it." Trust
  carried by specificity (finca, altitude, process, roast minutes, delivery day), not
  by reassurance copy.
- **Non-goals:** discount badges, product-photo card grids, carousels, floating
  "Buy now" bars, newsletter modals, emoji. None appear.

**The Direction Contract (frozen before tokens).** *Thesis:* a coffee magazine that
also sells the coffee. *Own-world:* a neighbourhood roaster's workshop — kraft paper,
printing ink, origin stamps, a brass scale. *Story:* "I chose my grind and my
frequency; the coffee arrives on Thursday, fresh, with the tasting note printed on the
label." *First viewport:* one enormous serif headline at the left over a 65ch text
column, and at the right the week's roast as a printed plate (origin, altitude, tasting
notes) — a single composition, no carousel. *Form:* paper #FAF7F2, ink #1A1815,
oxblood #7F1D1D used at most three times, radius 0.125rem, airy density, 96–128px
section air, ~95% neutral. *Finish:* 1px ink rules at 60%, no shadows, no gradients,
fades of 300–400ms, nothing bounces.

**The four commitments.**

1. **One chroma, spent on purpose.** Paper, ink and a kraft wash cover every surface;
   oxblood is the only hue and appears exactly three times per view — the price, the
   origin stamp and the subscription action. A fourth red is a defect.
2. **Structure is a rule, not a box.** Depth is a 1px ink rule at 60% (structure) or
   20% (row separators). There is no shadow token in the system and no component fill;
   even the printed plates are the paper with a rule around them.
3. **Two voices, one page.** A Georgia-class serif carries every word a human reads as
   prose; a Helvetica-class grotesque carries only 12px tracked captions, column heads,
   field labels and tabular prices. That split is the print convention the design is
   built on.
4. **The catalogue is an index, not a grid.** Five coffees are five numbered folios in
   a ruled list with tabular prices. There is no card, no image tile, no hover-reveal
   overlay — the folio list *is* the product.

**Substitution test (passed).** Swap the wordmark, the Spanish copy and the oxblood
hue and ask whether 80% of the page stays plausible for another product. It does not:
the first viewport is a roast label plate — origin, altitude, variety, process, roast
minutes, tasting note — which only a roaster prints; the catalogue is a numbered index
with "250 g, molido a pedido" and a folio number in the footer; the second board's
forms are a grind ballot and a delivery-frequency ballot whose options are *grind
settings* and *Thursday dates*; and the summary plate prices four Thursdays, not a
unit. None of those decisions survive a swap to a SaaS, a fashion label or a
restaurant.

## Colors

Three hue families inside the 3–5 ceiling — a neutral paper/ink/kraft ramp, one accent
(oxblood) and the same red as the status role. There is no second accent, no gradient,
no tinted card fill. ~95% of every surface is neutral by construction.

- **Paper (#faf7f2):** `background`, `card`, `popover`. Every surface is the sheet
  itself; plates separate by rule, never by fill (card-necessity rule). Nothing in the
  system needs a second surface color, so nothing declares one.
- **Printing ink (#1a1815):** `foreground`. All prose, display type and rules.
  16.58:1 on paper — the page never trades text contrast for softness.
- **Oxblood (#7f1d1d):** `primary`, `ring`-adjacent emphasis and `destructive`. 9.38:1
  on paper, so it is legal as a 30–36px price, as a filled button face (paper on it is
  the same 9.38:1) and as a 1px stamp border. It is *budgeted*: three spends per view,
  listed below.
- **Kraft (#f2ede4):** `secondary` and `muted`. Skeleton bars, pressed ballot rows,
  quiet surfaces. Ink on it measures 15.19:1.
- **Hover wash (#ebe4d8):** `accent`. Hover only, never a resting surface. Ink 14.02:1.
- **Warm gray (#5f574d):** `muted-foreground`. Captions, folio numbers, secondary
  lines. 6.65:1 on paper, 6.09:1 on kraft, 5.62:1 on the hover wash.
- **Rule ink (60% / 20%):** `border` and `border-faint`. 4.54:1 and 1.53:1 composited.
  A rule is structure and never carries text; `input` shares the 60% value because in a
  printed form the field boundary *is* the rule (both clear WCAG 1.4.11's 3:1).
- **Focus ink (#1a1815):** `ring`. Focus is ink, not red, so the accent budget survives
  keyboard navigation.

**The red budget, per view.** Board 01: the weekly price (250 g · $ 12.400), the round
origin stamp, the "Suscribirme" text action. Board 02: the order total ($ 36.400), the
filled `Empezar mi suscripción` button, the error label in the state strip. Hover
states never introduce red — a link hover is an ink underline.

Measured text pairs, all above the 4.5:1 floor:

| Pair | Ratio |
| --- | --- |
| `foreground` on `background` / `card` | 16.58:1 |
| `muted-foreground` on `background` | 6.65:1 |
| `muted-foreground` on `secondary` | 6.09:1 |
| `muted-foreground` on `accent` | 5.62:1 |
| `primary` on `background` · `primary-foreground` on `primary` | 9.38:1 |
| `foreground` on `secondary` | 15.19:1 |
| `foreground` on `accent` | 14.02:1 |
| `border` (composited) on `background` | 4.54:1 (rule, not text) |
| `border-faint` (composited) on `background` | 1.53:1 (rule, never text) |

### Design Tokens

```yaml
colors:
  # Paper and ink
  background: "#faf7f2"
  foreground: "#1a1815"
  card: "#faf7f2"
  card-foreground: "#1a1815"
  popover: "#faf7f2"
  popover-foreground: "#1a1815"
  # The single chroma, and its pressed value
  primary: "#7f1d1d"
  primary-foreground: "#faf7f2"
  primary-hover: "#6a1818"
  destructive: "#7f1d1d"
  destructive-foreground: "#faf7f2"
  # Kraft washes
  secondary: "#f2ede4"
  secondary-foreground: "#1a1815"
  muted: "#f2ede4"
  muted-foreground: "#5f574d"
  accent: "#ebe4d8"
  accent-foreground: "#1a1815"
  # Rules and focus
  border: "rgb(26 24 21 / 0.6)"
  border-faint: "rgb(26 24 21 / 0.2)"
  input: "rgb(26 24 21 / 0.6)"
  ring: "#1a1815"
```

## Typography

The ramp is the documented Tailwind paired scale (12, 14, 16, 18, 20, 24, 30, 36, 48,
60, 72 px with paired line heights) — carried unchanged, because a print page should
not invent sizes either. Two families, both locally available system stacks: a
Georgia-class serif for everything read as prose and a Helvetica-class grotesque for
12px metadata only. Nothing loads over the network; there is no FOUT and no font
licence surface.

- **Display (72/1, 60/1):** `-0.03em` tracking, weight 400. The storefront headline
  breaks as "Café del / jueves." — the break is part of the composition, not a wrap
  accident. No display step above 72px exists.
- **Headlines (36/40, 30/36, 24/32):** `-0.015em` tracking at 400. Hierarchy comes from
  size and the rule above the section, never from weight escalation.
- **Body:** 16/24 default, 20/28 for the standfirst, 18/28 for the plan narrative,
  14/20 for metadata. Measure capped at `65ch`; the plate's tasting note at `52ch`.
- **Labels:** 12/16 grotesque, uppercase, tracked `+0.14em` (nav, field labels, column
  heads, small print) or `+0.1em` (wordmark, ballot notes, footer, prices). Uppercase
  never exceeds 12px in this system.
- **Numerals:** prices, totals, dates and folio numbers use `font-variant-numeric:
  tabular-nums` in the grotesque. Georgia's old-style figures are why prices are not
  set in serif: a catalogue column must align.
- **Weights:** 400 and 500 only. 600 and 700 do not exist here — a printed page gets
  its emphasis from size, rule and italic, not from bold.
- **Italic:** reserved for two things — the tasting note on the label and the "nada se
  muele antes de que lo pidas" clause in the standfirst.

### Design Tokens

```yaml
typography:
  display-xl:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 72px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: -0.03em
  display-lg:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 60px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 36px
    fontWeight: 400
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 30px
    fontWeight: 400
    lineHeight: 36px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 24px
    fontWeight: 400
    lineHeight: 32px
    letterSpacing: -0.015em
  title-md:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 20px
    fontWeight: 400
    lineHeight: 28px
    letterSpacing: 0em
  body-lg:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 18px
    fontWeight: 400
    lineHeight: 28px
    letterSpacing: 0em
  body-md:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 16px
    fontWeight: 400
    lineHeight: 24px
    letterSpacing: 0em
  body-sm:
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif'
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
    letterSpacing: 0em
  label-sm:
    fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif'
    fontSize: 12px
    fontWeight: 500
    lineHeight: 16px
    letterSpacing: 0.14em
  label-xs:
    fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif'
    fontSize: 12px
    fontWeight: 500
    lineHeight: 16px
    letterSpacing: 0.1em
  figure-md:
    fontFamily: '"Helvetica Neue", Helvetica, Arial, sans-serif'
    fontSize: 16px
    fontWeight: 400
    lineHeight: 24px
    letterSpacing: 0em
    fontFeature: '"tnum" 1'
```

## Layout

A 4px ramp only, named by pixel value: 1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64,
80, 96, 128. This system never needs 28, 36, 44 or 56, so it does not declare them —
the temptation to nudge a gap by 3px is removed rather than managed.

- **Air:** section padding is 96px vertically (the contract's 96–128 range, at its
  tight end because a storefront index is read like a contents page, not a billboard).
  The masthead is 81px (24 + 32 + 24 + the bottom rule).
- **Container:** 1248px wide inside the 1440 board, with 32px inner padding → 1184px
  of usable column and 128px visual margins. Prose stops at 65ch; the label plate stops
  at 420px.
- **Storefront hero:** `minmax(0, 1fr) 420px` with a 96px gutter. The left column's
  facts row is pinned to the bottom of the plate, so the two columns end on the same
  line — an alignment device, not a coincidence.
- **Subscription page:** `minmax(0, 1fr) 416px` with a 96px gutter. The plan column is
  a form of ruled groups; the order plate is the only bordered rectangle on the page
  (together with the storefront's label plate — the two plates that carry printed
  information).
- **Catalogue index:** `56px | 1fr | 220px | 180px | 140px | 32px` with 24px gutters.
  Rows are 16px of vertical padding around a 28px line box plus the 20% ink rule
  (61px measured); prices are right-aligned on a shared edge with their column head.
- **Density (measured):** rows 61px, ballot choices 79px, fields 45px, the CTA 54px,
  the stamp 96px, nav links 25px — every target clears WCAG 2.2's 24px floor and every
  control clears the 44px advisory. Every interactive target is at least 44px tall, except the text links, which
  are inline prose links with 4px underline offset.

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
  space-32: 32px
  space-40: 40px
  space-48: 48px
  space-64: 64px
  space-80: 80px
  space-96: 96px
  space-128: 128px
  container-max: 1248px
  plate-width: 420px
  summary-width: 416px
  section-air: 96px
  gutter: 96px
  measure: 65ch
```

## Elevation & Depth

There is **no shadow in this system**. No `box-shadow` token exists, and no component
declares one — a shadow would read as a printing error on flat paper. Depth is
expressed three ways, in this order:

1. **The 60% ink rule** (`border`) for structure: the masthead's bottom edge, section
   heads, plate outlines, group dividers, the CTA's edge.
2. **The 20% ink rule** (`border-faint`) for rhythm: catalogue rows, plate field rows,
   ballot rows, legal lines. It is a lighter letterpress weight, not a separate color.
3. **The kraft wash** (`secondary`) for state, never for a resting surface: a pressed
   ballot row, a skeleton bar.

The two plates (the week's label on 01, the order summary on 02) are drawn as 1px 60%
ink outlines on the paper itself. They are the only rectangles with a full border; the
catalogue index deliberately has none, because the rows are a list, not a set of cards
(card-necessity rule). Paper grain is allowed by the contract at ≤3% but is omitted:
the only available implementations are a gradient stack or a filter, and gradients are
forbidden — flat paper is the honest choice.

## Shapes

One radius token, `0.125rem` (2px), with derived 1px and 4px steps and one pill. The
near-straight corner is the direction: this is a printed form, not a product card.
Every rectangle in both boards resolves through `var(--radius*)` or `0`.

- `sm` 1px — ballot marks, focus outlines, skeletons, row washes.
- `md` 2px — the plates, the button, the fields' optional inner radius.
- `lg` 4px — declared for a future floating layer; no artboard spends it.
- `none` 0 — the field underline and its zero-radius input box.
- `pill` 9999px — the round origin stamp **only**. A pill anywhere else is a bug: the
  near-straight corner is what makes the stamp read as a stamped seal rather than a
  badge.

### Design Tokens

```yaml
rounded:
  none: 0px
  sm: 1px
  md: 2px
  lg: 4px
  pill: 9999px
```

## Components

Components are defined by their states, not their resting look. Every interactive atom
carries hover, `:focus-visible`, `:active` and `:disabled`; focus is always a 2px ink
outline with a 2px offset (16.58:1 on paper) and is never suppressed.

- **Masthead.** 81px, a hairline at 60% ink, three zones: the tracked serif wordmark
  (24/32, `+0.1em`), four small-caps nav links with a 1px bottom border, and a dateline.
  The current link is marked by a 1px ink underline, not by color — red is budgeted.
  Hover: ink underline on the border token; active: muted text.
- **Display headline.** 72/1 at `-0.03em`, 400. It is the page's single bold move; the
  rest of the storefront is quiet. Never centered, never above an eyebrow badge.
- **Label plate (the roast label).** A 2px-radius rectangle, 1px 60% ink border, 32px
  padding. Rows: 12px small-caps label at 88px + serif value, separated by 20% ink
  rules. Foot: the 96px round stamp at the left, the 250 g note and the 30px oxblood
  price at the right, divided from the rows by a 60% rule.
- **Origin stamp.** 96px circle, 1px oxblood border, oxblood tracked caps, a 24px rule
  between the two lines. The only pill in the system, and the only element where a
  circle is allowed.
- **Catalogue index.** A real `<ol>` of five folios. Column heads are 12px small caps;
  rows are 20px serif names, 14px muted origins, 12px tracked processes, 16px tabular
  prices, and a hairline arrow that shifts 2px on row hover. Hover paints the row with
  the `accent` wash and underlines the name in ink. The whole row never becomes a card.
- **Ballots (grind, frequency).** Native radios and one checkbox, visually hidden but
  focusable; the visible mark is a 20px square with a 1px `input` border and a 12px
  filled inner square when checked. The label row is a ruled ballot line: 20px mark +
  16px gap + name + note. Hover paints the `accent` wash and darkens the mark border;
  `:active` paints the `secondary` wash; `:disabled` drops the whole row to 45% opacity
  with `cursor: not-allowed` and a reason in the note ("Sin molienda gruesa hasta el
  lote 48"). Focus draws the 2px ink ring on the *mark*, not on the invisible input.
- **Fields.** A printed line, not a box: no border except a 1px `input` underline,
  serif 18/28 value, 12px small-caps label above. Hover darkens the underline to ink;
  focus adds the 2px ink ring; disabled drops to 45% with `not-allowed`.
- **Order plate.** The summary: 20px title + `N° 4221` small caps, four detail rows,
  a strong rule before the math, two tabular subtotal rows, a strong rule before
  `$ 36.400` at 36px oxblood, then the 54px filled oxblood CTA (`Empezar mi
  suscripción`), which presses to `scale(0.97)` and mixes 8% ink on hover — never
  opacity, which would drop the label's contrast. Below it, 12px small print.
- **Designed states for the order plate.** Three states ship as an appendix strip, one
  per row: *vacío* (an em dash and "todavía no elegiste molienda"), *cargando* (two
  `secondary` skeleton bars at the price's geometry plus "calculando el envío…"), and
  *error* ("No pudimos calcular el envío" with an ink "Reintentar" link and a fallback
  to pickup). The visible plate is the populated state; the strip is the specimen
  sheet. Empty/loading/error are declared out of scope for the storefront's five-lot
  index, which is static by construction.
- **Motion.** Entrance fades 360ms `ease-out`, staggered 60ms, `opacity` only — nothing
  translates and nothing bounces. Micro-states are 180ms on `color`,
  `background-color`, `border-color`, `transform`. `prefers-reduced-motion: reduce`
  flattens every animation and transition to 1ms. Form controls get no entrance
  animation at all (frequency-gated motion).
- **Declared but unspent roles.** `popover` / `popover-foreground`, `rounded.lg` and
  the destructive pair are declared so a future floating layer or a confirmation step
  cannot invent its own surface or its own red. No artboard renders a popover, and no
  artboard shows a destructive action: the only red status on either board is the
  summary plate's 12px `Error` label, which shares the accent's value because this
  direction owns one chroma.
- **Browser surfaces.** `::selection` is the `accent` wash with ink text; links use a
  1px underline at 4px offset; scrollbars are left native.

### Design Tokens

```yaml
components:
  page:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
  masthead:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    height: 81px
    padding: 24px
  wordmark:
    textColor: "{colors.foreground}"
    typography: "{typography.headline-sm}"
  navlink:
    textColor: "{colors.foreground}"
    padding: 4px
    typography: "{typography.label-sm}"
  navlink-current:
    textColor: "{colors.foreground}"
    typography: "{typography.label-sm}"
  display-title:
    textColor: "{colors.foreground}"
    typography: "{typography.display-xl}"
  standfirst:
    textColor: "{colors.foreground}"
    typography: "{typography.title-md}"
  label:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-sm}"
  fact-label:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-xs}"
  fact-value:
    textColor: "{colors.foreground}"
    typography: "{typography.body-sm}"
  rule-strong:
    backgroundColor: "{colors.border}"
    height: 1px
  rule-faint:
    backgroundColor: "{colors.border-faint}"
    height: 1px
  plate:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    rounded: "{rounded.md}"
    padding: 32px
  plate-row:
    textColor: "{colors.foreground}"
    padding: 8px
    typography: "{typography.body-sm}"
  plate-note:
    textColor: "{colors.foreground}"
    typography: "{typography.body-sm}"
  stamp:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    rounded: "{rounded.pill}"
    height: 96px
    typography: "{typography.label-xs}"
  weekly-price:
    textColor: "{colors.primary}"
    typography: "{typography.headline-md}"
  catalogue-column-head:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-xs}"
  catalogue-row:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    padding: 16px
    typography: "{typography.title-md}"
  catalogue-row-hover:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-foreground}"
  catalogue-origin:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.body-sm}"
  catalogue-process:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-xs}"
  catalogue-price:
    textColor: "{colors.foreground}"
    typography: "{typography.figure-md}"
  text-action:
    textColor: "{colors.primary}"
    padding: 8px
    typography: "{typography.label-sm}"
  text-action-hover:
    textColor: "{colors.primary-hover}"
    typography: "{typography.label-sm}"
  crumbs:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-xs}"
  crumbs-current:
    textColor: "{colors.foreground}"
    typography: "{typography.label-xs}"
  group-legend:
    textColor: "{colors.foreground}"
    typography: "{typography.label-sm}"
  group-hint:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-xs}"
  ballot-choice:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    padding: 16px
  ballot-choice-hover:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.accent-foreground}"
  ballot-choice-pressed:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
  ballot-mark:
    backgroundColor: "{colors.background}"
    rounded: "{rounded.sm}"
    size: 20px
  ballot-mark-selected:
    backgroundColor: "{colors.foreground}"
    rounded: "{rounded.sm}"
    size: 12px
  ballot-note:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.body-sm}"
  ballot-choice-disabled:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.body-sm}"
  field:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    height: 45px
    padding: 8px
    typography: "{typography.body-lg}"
  field-label:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-sm}"
  field-boundary:
    backgroundColor: "{colors.input}"
    height: 1px
  focus-ring:
    backgroundColor: "{colors.ring}"
    size: 2px
  order-plate:
    backgroundColor: "{colors.card}"
    textColor: "{colors.card-foreground}"
    rounded: "{rounded.md}"
    padding: 32px
  order-row:
    textColor: "{colors.foreground}"
    padding: 12px
    typography: "{typography.body-sm}"
  order-row-label:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-sm}"
  order-total:
    textColor: "{colors.primary}"
    typography: "{typography.headline-lg}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    height: 54px
    padding: 16px
    typography: "{typography.label-xs}"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    height: 54px
    typography: "{typography.label-xs}"
  popover:
    backgroundColor: "{colors.popover}"
    textColor: "{colors.popover-foreground}"
    rounded: "{rounded.lg}"
    padding: 12px
    typography: "{typography.body-sm}"
  button-destructive:
    backgroundColor: "{colors.destructive}"
    textColor: "{colors.destructive-foreground}"
    rounded: "{rounded.md}"
    height: 54px
    padding: 16px
    typography: "{typography.label-xs}"
  small-print:
    textColor: "{colors.muted-foreground}"
    typography: "{typography.label-xs}"
  state-empty:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    padding: 16px
    typography: "{typography.body-md}"
  state-loading-skeleton:
    backgroundColor: "{colors.muted}"
    rounded: "{rounded.sm}"
    height: 12px
  state-error:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    padding: 16px
    typography: "{typography.body-md}"
  state-error-label:
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
  colophon:
    backgroundColor: "{colors.background}"
    textColor: "{colors.muted-foreground}"
    padding: 48px
    typography: "{typography.label-xs}"
```

## Do's and Don'ts

- Do spend oxblood exactly three times per view, and name the three spends in the
  tradeoff: price, stamp, action on 01; total, action, error on 02. Don't add a fourth
  red for a hover state, a link, or an active nav item — those are ink.
- Do build structure with the 60% ink rule and rhythm with the 20% ink rule. Don't add
  a shadow, a card fill, or a tinted surface; if a rule can express the boundary, the
  boundary is a rule.
- Do keep the catalogue as an index of numbered folios with tabular prices. Don't turn
  it into a card grid or add product photography — the label *is* the photograph.
- Do set prose in the serif and metadata in the 12px tracked grotesque. Don't set a
  price in the serif (Georgia's old-style figures break column alignment) and don't set
  prose in the grotesque.
- Do keep uppercase at 12px or below with `+0.1em` to `+0.14em` tracking. Don't use an
  uppercase eyebrow above the display headline; the label plate carries the context.
- Do keep one radius family (1/2/4px) and reserve 9999px for the origin stamp. Don't
  give buttons, fields or plates a pill radius.
- Do keep focus ink and 2px + 2px offset on every interactive element, including the
  invisible radio input's visible mark. Don't remove an outline without a visible
  replacement.
- Do fade in at 360ms, `opacity` only, and stop entirely under `prefers-reduced-motion`.
  Don't translate, bounce or spring; paper does not move.
- Do keep prices, totals, dates and folios tabular and right-aligned on a shared edge.
  Don't center a numeric column or mix proportional digits into a list.
- Do design the order plate's empty, loading and error states when the plate changes;
  the storefront index is explicitly out of scope because it is static.
- Do keep the substitution test before adding a section: if the block would read the
  same with another company's wordmark, it is template furniture — replace it with
  something only a roaster prints (a roast date, an altitude, a grind ballot).
- Don't introduce gradients, glass, illustrations, emoji icons, or a second accent.
  The page's decoration budget is a rule and a round stamp, and that is deliberate.
