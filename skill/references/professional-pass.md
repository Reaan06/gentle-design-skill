# The Professional Pass — full pre-delivery checklist

Run top to bottom before reporting an artboard done. Every item is mechanical: it can
be checked by reading the artboard's CSS/markup. Evidence refs point to `evidence.md`.

## A. Foundation

- [ ] A1 `:root` holds the full semantic token block: `background/foreground/card/
      primary/secondary/muted/accent/destructive/border/input/ring` + `--radius`
      (E1, E7).
- [ ] A2 No raw hex/px values in component CSS except inside `:root` and calc derivations.
- [ ] A3 Dark mode (if present) re-maps the same roles; no hard-coded dark colors in components.
- [ ] A4 ≤2 font families total; body ≥14px; body line-height 1.4–1.6 (E4 hint, Figma/Make practice).
- [ ] A5 3–5 colors total: 1 primary + 2–3 neutrals + 1–2 accents/status (E4, E6).

## B. Typography

- [ ] B1 Only documented ramp steps (12/14/16/18/20/24/30/36/48/60/72 + paired line-heights, E7).
- [ ] B2 Display sizes (≥48px) use `line-height: 1` and negative tracking (−0.02…−0.04em).
- [ ] B3 No skipped ramp steps between adjacent text roles.
- [ ] B4 Body measure ≤ `65ch`–`80ch` (E8).
- [ ] B5 `tabular-nums` (`font-variant-numeric: tabular-nums`) on any aligned/comparing numbers (E3).
- [ ] B6 Uppercase labels (if any) have loose tracking (+0.05em or more) and are ≤ `text-xs` (E8).
- [ ] B7 Hierarchy by size/weight/color-role, not all-bold; secondary text uses
      `muted-foreground`-style gray.

## C. Color & surface

- [ ] C1 ~90% of surface area is neutral (E6); brand/primary color only on primary
      actions, active states, small accents.
- [ ] C2 `--primary` (or brand accent) appears on ≤3 prominent elements per view.
- [ ] C3 Status hues (green/amber/red) only mark real status; nothing decorative is status-colored.
- [ ] C4 No unrequested purple/violet gradient; gradients (if any) are ≤3 analogous
      stops at low alpha, or texture (dot grid / hairline / glow) instead (E2, E4).
- [ ] C5 Contrast ≥4.5:1 normal text, ≥3:1 large text and UI controls (WCAG AA; E5 lint).

## D. Spacing & layout

- [ ] D1 All spacing from the 4px ramp (allowed steps 1,2,4,8,12,16,20,24,32,40,48,64,80,96,128).
- [ ] D2 Gaps via `gap`/margins on one axis; no magic offsets to fake alignment.
- [ ] D3 Landing sections breathe ≥96px vertically; app layouts 24–32px section gaps (E2).
- [ ] D4 Optically aligned within ±1px: icon boxes, checkbox rows, numeric columns (E3).
- [ ] D5 Tap targets ≥44×44px on touch-shaped layouts (E8; WCAG 2.2 floor 24px).

## E. Radius & elevation

- [ ] E1 One `--radius` token + derived variants; pills `9999px`; no arbitrary radii.
- [ ] E2 Structure by 1px `--border`; shadows only on genuinely floating layers, alpha ≤0.12.

## F. States & motion

- [ ] F1 Every interactive element: hover (subtle bg shift), `:focus-visible` (2px
      `--ring`, offset), active, disabled (reduced opacity + not-allowed).
- [ ] F2 Empty, loading, and error states designed or explicitly declared out of scope (E3).
- [ ] F3 Micro-transitions 100–250ms ease-out; entrances 300–500ms, stagger 40–80ms (E8).
- [ ] F4 Only `transform`/`opacity` animated; no `transition: all` (E3).
- [ ] F5 `prefers-reduced-motion` block present when any animation exists.
- [ ] F6 Press feedback on pressables: `:active` scale ≈0.97 (E8).

## G. Anti-slop (see generic-vs-professional.md)

- [ ] G1 No default indigo/purple gradient hero, no 3-identical-icon-card row unless
      the content demands it, no emoji-as-icon, no decorative badge/pill spam.
- [ ] G2 One focal "bold" element per design; everything else quiet (E8).
- [ ] G3 Substitution test fails: swapping name + logo + accent would NOT leave 80%
      of the page equally plausible for another product (E10).
- [ ] G4 No mechanical tells: colored card top/left stripes, badge-above-H1,
      decorative `01/02/03` markers on non-sequences, emoji icons, identical card
      rows, single-default-font dominance (E10).

## H. Critique loop

- [ ] H1 Run the deterministic gate first — `python3 <skill-path>/scripts/design-gate.py
      <artboard.html>` — and fix all its findings **before** the render-critique loop.
      Then render the artboard, screenshot it (canvas or agent-browser), critique against
      the brief and this checklist, fix, re-check once (E8, E10).
- [ ] H2 Compare against `design/system.md` tokens when the project has one.

### Deterministic gate (`scripts/design-gate.py`)

Mechanical half of this checklist, executable: Python 3 standard library only, no
browser, no network. Exit `0` clean, `1` findings, `2` usage error; findings print as
`file:line [RULE name] message` (E10, vercel-labs web-interface-guidelines format).
`--json` emits `{file, findings:[{rule,line,message}]}` (an array for multiple files).

| Rule | Fails when | Checklist |
| --- | --- | --- |
| R1 `token-block` | `:root` lacks any of `background/foreground/card/primary/secondary/muted/accent/destructive/border/input/ring/radius` (or no `:root` at all) | A1, A2 |
| R2 `raw-color-outside-root` | hex / `rgb()` / `hsl()` / `oklch()` literal outside `:root` | A2, A3 |
| R3 `off-ramp-spacing` | `margin`/`padding`/`gap` px value off the 4px ramp | D1 |
| R4 `transition-all` | `transition: all` or `transition-property: all` | F4 |
| R5 `missing-reduced-motion` | `@keyframes`/`animation` present, no `prefers-reduced-motion` block | F5 |
| R6 `missing-focus-visible` | interactive elements present, no `:focus-visible` rule | F1 |
| R7 `font-tell` | `Inter` or `Roboto` is the first family in a `font-family` | A4 |
| R8 `slop-palette` | indigo/violet slop hex (`6366f1`, `8b5cf6`, `a855f7`, `7c3aed`) in a gradient | C1, C4 |
| R9 `emoji-icon` | emoji codepoint used as icon inside `<button>`/`<a>`/`<nav>` | G1, G4 |
| R10 `numbered-markers` | `01`–`09` marker at the start of a heading or a `.index`/`.num`/`.step` element — **review flag only**, the gate cannot know whether it is a real sequence | G4 |
| R11 `radius-drift` | `border-radius` literal not `var(--radius*)`, `calc(var(--radius) …)` or `9999px` | E1 |
| R12 `transition-duration-tell` | transition duration > 500ms (animation entrances are not counted) | F3 |

Deliberate allowances, so the gate stays quiet on legitimate systems: raw colors inside
`:root` and inside token re-map blocks (`[data-theme=…]`, `.dark`,
`@media (prefers-color-scheme: …)`); `calc()` token derivations for color and spacing;
negative ramp-step margins; arrows/`⌘`/`⇧` and `<kbd>` glyphs (not emoji).

Limits: durations and colors behind `var()` cannot be evaluated statically; the type
and size ramps need semantic intent and stay with B1/B3; a finding is a review prompt,
not a verdict — fix it or name the deviation and why (Hard Rule 1).
