# Dark Mode — the same roles, re-mapped

Dark mode is not a second design system. It is the **same eleven semantic roles**
(`--background`, `--foreground`, `--card`, `--primary`, `--secondary`, `--muted`,
`--accent`, `--destructive`, `--border`, `--input`, `--ring`) with new *values*.
Components never learn that dark mode exists (E1 — shadcn/theming keeps one variable
contract and swaps the theme; E5 — Stitch's `design.md` freezes `colorMode` as a theme
input, never inside component prompts).

Rule of thumb: if a component declares a dark-looking literal (`#111`, `#e5e5e5`,
`rgba(255,255,255,.08)`), the design is wrong — that value belongs in the theme block.

## 1. Role mapping

Capture-based reference (Pulse Analytics, the project's dark artboards `04`/`05`); every
ratio below is measured from the token values, not estimated.

| Role | Light | Dark | Why it changes |
| --- | --- | --- | --- |
| `--background` | `#ffffff` | `#0c100f` (oklch `0.168 0.007 179`) | near-black, low chroma, same hue family as the accent |
| `--foreground` | `#0b1210` | `#e9efed` (oklch `0.947 0.007 174`) | not pure white — see §3 |
| `--card` | `#ffffff` | `#1c2221` (L `0.246`) | elevation is a lightness step, not a shadow |
| `--popover` | `#ffffff` | `#232a29` (L `0.278`) | one step above card, same ladder |
| `--primary` | `#0b5f4f` | `#5fd6b8` (L `0.800`) | inverts: a light pill on dark (§2.5) |
| `--primary-foreground` | `#ffffff` | `#05100d` (L `0.160`) | text on the inverted primary must be dark |
| `--secondary` | `#f3f6f5` | `rgb(255 255 255 / 0.06)` | a wash, not a color: works on any dark step |
| `--muted` | `#f3f6f5` | `rgb(255 255 255 / 0.06)` | same value as `--secondary`, as in light |
| `--muted-foreground` | `#596663` | `#9daba7` (L `0.729`) | mid-light gray; must clear 4.5:1 on every dark surface |
| `--accent` | `#eaf0ee` | `rgb(255 255 255 / 0.08)` | hover wash, one alpha step above `--secondary` |
| `--destructive` | `#a5231b` | `#f4786a` (L `0.714`) | a dark red loses contrast on dark; lighten it |
| `--destructive-foreground` | `#ffffff` | `#170604` | the light red needs dark text on it |
| `--border` | `#e1e6e4` | `rgb(255 255 255 / 0.12)` | 8–14% white replaces the gray ramp |
| `--input` | `#7f8c88` | `rgb(255 255 255 / 0.38)` | control boundaries must still clear 3:1 (§2.3) |
| `--ring` | `#0b5f4f` | `#8be8d2` (L `0.867`) | focus must read on near-black, so it lightens |

## 2. Mapping rules

### 2.1 Canvas: near-black, low chroma, tinted by the accent hue
- `--background` sits at **oklch L `0.145`–`0.205`**, chroma `≤ 0.012`. Pure `#000` is
  out: it kills every border and raises halation on light text.
- Keep the accent's hue angle (Pulse: `H 179`) instead of neutral gray. A 0.007-chroma
  tint reads as "designed black" and makes the accent look native.
- The light theme's white canvas and the dark theme's near-black are the *same* role:
  one value flips, nothing else in the stylesheet moves.

### 2.2 Surfaces elevate by lightness (`background → card → popover`)
- Steps of **L +0.05 to +0.08** per layer (Pulse: `0.168 → 0.246 → 0.278`).
- A card on dark is `--card` fill + 1px `--border`; it is **not** a shadow and **not**
  a lighter border-only card (the light convention) — dark needs fill separation.
- Relative order matters more than absolute values. If a wash (`--secondary` at 6%
  over background = L `0.231`) is lighter than `--card` (L `0.246`), a pressed/selected
  chip drawn in `--card` on a `--secondary` track will read *sunken*. Fix the ladder,
  not the component.
- `--popover` is the top of the ladder and inherits the same ladder on any parent.

### 2.3 Borders: low-alpha white, not a gray value
- `--border: rgb(255 255 255 / 0.08–0.14)`. Alpha means one border token works on the
  canvas, on a card and on a popover without three gray variants.
- Structural hairlines are exempt from contrast rules (Pulse: `1.37:1` on the canvas vs
  light's `1.26:1` — deliberately matched perceptibility).
- `--input` is the exception: WCAG 1.4.11 needs **3:1 for interactive boundaries**, so
  it climbs to `0.34–0.40` white (Pulse: `0.38` → `3.56:1` on canvas, `3.51:1` on card,
  `3.41:1` on popover). Dark input borders are therefore visibly stronger than dark
  hairlines; that asymmetry is correct and mirrors light (`#7f8c88` = `3.49:1`).
- Semi-transparent dividers derived with `color-mix(in oklab, var(--border) 50%,
  var(--background))` still behave: the mix is premultiplied, so the row divider lands
  at ~6% white over the canvas. Do not "fix" it with an extra hex.

### 2.4 Washes: white at 4–8% alpha
- `--secondary`/`--muted` = **4–6%**, `--accent` (hover) = **6–8%**. Two steps only;
  more than two hover washes and the UI starts to shimmer.
- Because they are alpha, a wash over `--card` is automatically stronger than the same
  wash over `--background` (`0.06` → L `0.300` on card vs L `0.231` on canvas). That is
  the desired behavior: hover on a raised surface should still be visible.
- Selected rows/tree items use the wash, not a tinted accent; keep `--primary` for the
  active indicator (2px bar, dot, check) so color still means "state".

### 2.5 Primary inverts — pick one of two strategies, name it
- **(a) Light pill on dark** (Pulse): primary becomes a light accent
  (`#5fd6b8`, L `0.800`) with a dark `--primary-foreground` (`#05100d`, `10.86:1`).
  Best when the product has one hero action per view.
- **(b) Accent-tinted dark**: primary stays a *dark* accent with light text
  (`--primary` L `0.30–0.40`, fg L `0.95`). Only valid if the resulting fg pair clears
  4.5:1 — most brand hues fail here, which is why shadcn's dark default abandons brand
  color and uses near-white.
- Never reuse the light theme's dark teal on a dark canvas: `#0b5f4f` on `#0c100f` is
  `1.9:1`, invisible as an action surface.
- `--ring` lightens *independently* of the primary (focus is not a brand moment):
  Pulse `#8be8d2` at `13.29:1`.

### 2.6 Destructive: lighten, then re-check
- Light `#a5231b` (L `0.40`) collapses on dark. Move to **L `0.65–0.75`**
  (Pulse `#f4786a`, L `0.714`): `7.06:1` on canvas, `5.95:1` on card, `6.45:1` on its
  own 8% wash.
- `--destructive-foreground` becomes dark (`#170604`, `7.27:1`) because the fill is now
  light. A white label on a light-red dark-mode button is a defect (`2.33:1`).
- Status washes keep their low alpha (6–8%) but must be re-measured: red at 8% *raises*
  the canvas luminance, so the delta is small but real (`6.62:1` → `6.45:1`).

### 2.7 Foreground and muted text
- `--foreground` in **oklch L `0.92–0.97`**, chroma `≤ 0.01`, hued with the canvas.
  Pure `#fff` on `#000` gives `21:1`, which is worse than it looks: it halos on OLED
  and flattens hierarchy.
- `--muted-foreground` must clear 4.5:1 **on the darkest surface it lands on**, not on
  the canvas. Pulse muted is `8.04:1` on canvas but `6.78:1` on card, `6.15:1` on
  popover and `5.71:1` on a 6% wash over card — all still AA, with the headroom
  intentional because dark antialiasing eats thin text.
- `--ring` follows the *ink*, not the primary: it is the lightest interactive value in
  the theme (L `≥ 0.80`) so the 2px outline survives on canvas **and** on the lightest
  surface (Pulse `#8be8d2`: `13.29:1` on canvas, `11.21:1` on card).

## 3. Contrast — computed on the dark pairs

AA on dark: **4.5:1 body, 3:1 large text and UI controls.** Measure the pair that will
actually render, after alpha compositing (a token value like `rgb(255 255 255 / .06)`
has no contrast on its own — composite it over its parent surface first).

| Pair (Pulse dark) | Ratio | Requirement |
| --- | --- | --- |
| `--foreground` on `--background` | 16.44:1 | AA body ✓ |
| `--foreground` on `--card` | 13.87:1 | AA body ✓ |
| `--foreground` on `--popover` | 12.57:1 | AA body ✓ |
| `--muted-foreground` on `--background` | 8.04:1 | AA body ✓ |
| `--muted-foreground` on `--card` | 6.78:1 | AA body ✓ |
| `--muted-foreground` on `--popover` | 6.15:1 | AA body ✓ |
| `--muted-foreground` on 6% wash over card | 5.71:1 | AA body ✓ |
| `--primary` on `--background` | 10.76:1 | AA body ✓ |
| `--primary-foreground` on `--primary` | 10.86:1 | AA body on fill ✓ |
| `--destructive` on `--background` | 7.06:1 | AA body ✓ |
| `--destructive` on `--card` | 5.95:1 | AA body ✓ |
| `--destructive` on its own status wash | 6.45:1 (8% on canvas) · 6.50:1 (8% on card) | AA body ✓ |
| `--ring` on `--background` / `--card` | 13.29 / 11.21:1 | 3:1 focus indicator ✓ |
| `--input` (38% white) on `--background` | 3.56:1 | 1.4.11 UI boundary ✓ |
| `--border` (12% white) on `--background` | 1.37:1 | hairline, exempt (non-text) |

Composite ladder for this canvas (measured, so a reviewer can check a value by eye):

| White alpha over `#0c100f` | Result | L | Ratio vs canvas |
| --- | --- | --- | --- |
| 4% | `#161a19` | 0.213 | 1.09:1 |
| 6% (`--secondary`/`--muted`) | `#1b1e1d` | 0.231 | 1.14:1 |
| 8% (`--accent`) | `#1f2322` | 0.252 | 1.21:1 |
| 12% (`--border`) | `#292d2c` | 0.293 | 1.37:1 |
| 38% (`--input`) | `#686b6a` | 0.525 | 3.56:1 |

Two traps: (1) do not lift `--muted-foreground` to compensate for a *border* that is
too dark — fix the border; (2) re-measure after any wash change, since every alpha
token shifts the surface under the text.

## 4. Elevation: lightness steps, not shadow

Shadows are near-invisible on dark (black on black carries no signal), so elevation is
encoded by **surface L + a 1px lighter border** (E6 — Figma's surface-color hierarchy
over borders is the same idea inverted for dark).

Algorithmic approach, from Linear's redesign (E10): *"instead of having to define 98
specific variables for each theme, we defined three: base color, accent color, and
contrast"* — the theme is **derived in LCH from three inputs**, not hand-authored per
token. Practical encoding for artboards:

1. Fix three inputs: base (canvas hue + L), accent (hue + chroma), contrast (how far
   ink and surfaces travel from base).
2. Derive every surface as an L step of base; derive every border/wash as an alpha of
   the ink color; derive text as base ± contrast.
3. Because L is the elevation axis, adding a surface means adding a step — never a new
   shadow, never a new gray.

When a layer genuinely floats (popover, modal, command palette), dark shadows still
work if they are *deep* and paired with a ring:

```css
--shadow-popover: 0 4px 6px -1px rgb(0 0 0 / 0.5), 0 0 0 1px rgb(255 255 255 / 0.10);
--shadow-modal: 0 20px 25px -5px rgb(0 0 0 / 0.6), 0 0 0 1px rgb(255 255 255 / 0.10);
```

Alpha goes **up** on dark (light's `≤0.12` reads as nothing on black; `0.5–0.6` is the
equivalent), and the inset ring replaces the light theme's hairline. Panes, cards,
rows and bands still get **no** shadow.

## 5. Motion and texture

- Durations and easings do **not** change between themes (`120/180/320ms`,
  `--ease-out`, `scale(0.97)` press). Contrast flips, timing does not.
- **Halve the alpha** of any glow, radial gradient or dot grid: a 6% white dot grid on
  white is subtle; on `L 0.168` the same 6% is roughly twice the perceptual lift. Light
  `6%` → dark `3–4%`; light radial accent glow `≤10%` → dark `≤5%`.
- Keep glow geometry identical so the artboard reads as the same design.
- Glows are decoration: they must animate on `opacity` only (never `filter: blur` per
  frame) and disappear under `prefers-reduced-motion: reduce`.
- Dark surfaces amplify banding: if a gradient is visible, add `≤3%` noise or drop it.

## 6. Media strategy — three entry points, one declaration set

The *same* declarations must be reachable three ways, never duplicated by hand:

```css
/* 1. System preference (the default contract) */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* dark token values */ }
}
/* 2. Explicit pin — user toggle, or a static artboard/screenshot */
:root[data-theme="dark"] { /* identical dark token values */ }
/* 3. Dark is the product default (dev tools, IDEs, desktop apps) */
@media (prefers-color-scheme: light) {
  :root:not([data-theme="dark"]) { /* light token values */ }
}
```

- Pick **one owner** per project: tokens live in `:root` (light) + one dark block. Never
  theme in JavaScript on first paint (FOUC); JS may only write `data-theme`.
- Always declare `color-scheme: dark` (or `light dark`) — form controls, scrollbars and
  the canvas background otherwise stay light. `<meta name="color-scheme">` belongs in
  `<head>`.
- **Static artboards** (this project's `04`/`05`) hard-pin dark in `:root` and set
  `data-theme="dark"` on `<html>`: a screenshot must be deterministic regardless of the
  viewer's OS. The file carries the media block as a comment-level pointer to this
  section; the runtime ships the real `@media` rule.
- Test both entry points: `prefers-color-scheme` (emulated in DevTools) **and** the
  `data-theme` pin. A board that only works under one of them has two themes, not one
  system.
- `prefers-color-scheme` is a *preference*, not a guarantee of display quality: keep
  AA contrast in both directions, don't auto-invert images, don't force-dark a light
  brand surface.

## 7. Failure modes seen in generated output

| Symptom | Cause | Fix |
| --- | --- | --- |
| `#000` canvas, `#fff` text | pure-black default | L `0.145–0.205` canvas, L `0.92–0.97` ink |
| Cards invisible / grey boxes | or `#1a1a1a` for every surface | one L step per layer + 1px alpha border |
| White 3% borders | light alpha reused | 8–14% white; `--input` to 3:1 |
| Brand teal CTA unreadable | light primary reused | invert primary (§2.5) |
| Red status dim | dark red on dark canvas | L `0.65–0.75` red + dark fg |
| Muddy hover on cards | wash alpha copied from canvas usage | one wash token, alpha over parent |
| Focus ring vanishes | ring kept from light | ring L `≥0.8`, 2px + offset |
| Glow blown out | same alpha as light | halve it |
| Theme flash on load | JS-owned theme | `:root` + media block, `color-scheme` |
| Components with `#111` literals | dark hard-coded | move every value into the role |

## 8. Dark-mode checklist (10 items)

- [ ] **D1** Dark values exist for **all eleven roles** (+ their `-foreground` pairs) in
      one theme block; no component declares a dark literal or a raw color.
- [ ] **D2** `--background` is near-black and low-chroma (oklch L `0.145–0.205`, C
      `≤ 0.012`), hued with the accent — not `#000`, not neutral gray.
- [ ] **D3** Surfaces ascend by lightness (`background → card → popover`, +`0.05–0.08`
      L per step), shadows are absent from structure and reserved for floating layers.
- [ ] **D4** `--border` is low-alpha white (8–14%); `--input` is lifted until it clears
      **3:1** against every surface it bounds (1.4.11).
- [ ] **D5** `--secondary`/`--muted`/`--accent` are white washes at 4–8% alpha; the wash
      ladder stays *below* `--card` when a selected chip is drawn on a wash track.
- [ ] **D6** `--primary` is inverted by a named strategy (light pill with dark fg, or
      accent-tinted dark with AA-checked fg); `--ring` lightens independently and keeps
      3:1.
- [ ] **D7** `--destructive` is lightened to L `0.65–0.75` with a dark
      `--destructive-foreground`, measured on canvas, card and its own status wash.
- [ ] **D8** Every text pair measured **after compositing** on dark: ≥4.5:1 body,
      ≥3:1 large/UI; `--foreground` sits at L `0.92–0.97`, never pure white.
- [ ] **D9** Glow/dot-grid/gradient alphas are halved vs light; motion durations,
      easings, press feedback and the `prefers-reduced-motion` block are unchanged.
- [ ] **D10** Both entry points work (`@media (prefers-color-scheme: dark)` and the
      `data-theme` pin), `color-scheme` is declared, and no `<script>` owns the theme.
