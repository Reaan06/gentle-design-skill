# Composition Patterns & Decision Trees (Figma Make Kits + Agent REA)

Evidence: `evidence.md` §E6, §E11, §E12.

Atomic tokens (`--primary`, `--border`, `--radius`) prevent raw-value drift, but
isolated atoms do not produce coherent screens on their own (E12: Figma Help Center).
Agents compose reliably when given **higher-order block rules**, **ASCII decision
trees**, **frequency budgets**, and **`CORRECT / WRONG` pairs**.

---

## 1. Layout Intent & Sizing Contract (Figma Auto Layout → CSS)

Every block in an artboard must declare its sizing intent explicitly rather than
relying on accidental content width:

| Figma Auto Layout | CSS Equivalent | When to Use |
| --- | --- | --- |
| `Fill container` | `width: 100%` or `flex: 1 1 0%; min-width: 0` | Main content panes, table rows, form inputs, banners, stacked mobile actions |
| `Hug contents` | `width: fit-content; flex-shrink: 0` | Buttons, chips, badges, inline metadata tags |
| `Fixed sizing` | Explicit `width` / `height` + `flex-shrink: 0` | Avatars, 40–48px icon rails, leading icon boxes (20×20 / 40×40) |
| `Min / Max bounds` | `min-width: 0; max-width: 65ch` (or `1120px`) | Prose columns, split panes, command overlays (prevents flex blowout & long lines) |

Rule: any flex or grid child holding truncatable text or tables MUST include
`min-width: 0` so long tokens never force horizontal overflow.

---

## 2. Decision Trees (Make Kits style)

### 2.1 Surface vs. Border Hierarchy

Figma's live sites (`E11`) and Make Kits `color.md` (`E12`) keep non-interactive
layout wrappers borderless unless framing is intentional, separating regions through
**spacing air** and **surface contrast** instead of boxing every block.

```text
┌─ "Does this container need a border?"
│
├─ Interactive control (input, select, textarea, clickable card, toggle)?
│  └─ YES -> 1px solid var(--input) or var(--border); hover/focus uses var(--ring)
│
├─ Standalone floating layer (popover, dropdown, modal, command palette)?
│  └─ YES -> var(--popover) + 1px solid var(--border) + floating shadow
│
├─ Sidebar or split desktop pane boundary?
│  └─ YES -> 1px solid var(--border) on the dividing edge only (border-right / border-bottom)
│
├─ Card sitting on the same color canvas (e.g. white card on white background)?
│  └─ CHECK CARD-NECESSITY FIRST: if spacing + type creates grouping, drop the card!
│     If it truly is a distinct data unit -> 1px solid var(--border) (no heavy fill/shadow)
│
└─ Outer section, header, metric wrapper, or nested layout group?
   └─ NO -> use whitespace (48–96px air) or surface step (var(--muted) vs var(--card))
```

### 2.2 Button Variant & Action Group Tree

Never invent arbitrary button styles on the fly. Lock every design to a closed
variant set and obey the Make Kits frequency distribution:

| Variant | Target Share | Role | Surface / Text |
| --- | --- | --- | --- |
| `primary` | ~20–30% (max 1 per visible section, ≤3 per view) | Main CTA / submit / create | `var(--primary)` bg + `var(--primary-foreground)` text |
| `neutral` (`secondary`) | ~50% (default) | Supporting actions, Cancel, Back, toolbar actions | `var(--secondary)` or `var(--card)` + `var(--foreground)` + `1px solid var(--border)` |
| `subtle` (`ghost`) | ~20% | Low-emphasis actions, row triggers, close buttons | `transparent` bg (hover `var(--accent)`) + `var(--foreground)` |
| `destructive` | <5% (confirmation/danger only) | Delete, revoke, irreversible action | `var(--destructive)` + `var(--primary-foreground)` (or tinted inline text) |

```text
┌─ "Which button variant and placement should I use?"
│
├─ Primary outcome of this screen or section (only ONE)?
│  └─ primary -> place on the RIGHT in horizontal groups (Cancel left, Save right)
│
├─ Supporting action beside a primary button (Cancel, Back, Export, Filter)?
│  └─ neutral (secondary) -> MUST match the primary button's height/size
│
├─ Repeated row action, icon-only toolbar action, or tertiary link-like trigger?
│  └─ subtle (ghost) -> never compete with primary
│
└─ Irreversible removal or danger confirmation?
   └─ destructive -> isolate from primary; never style routine saves red
```

### 2.3 Text Hierarchy & Scale-Before-Opacity

Make Kits explicitly forbids washing out large labels with low opacity to fake
hierarchy (`E12`). Drop size/weight step first, keeping readable foreground ink:

```text
┌─ "How do I de-emphasize secondary information?"
│
├─ Primary headline / body / metric value?
│  └─ Full foreground: var(--foreground) at step size (16px–72px)
│
├─ Supporting description, subtitle, table header, form hint?
│  └─ Smaller step (14px or 12px) + var(--muted-foreground) (still ≥4.5:1 WCAG AA)
│
├─ Text or icon inside a solid var(--primary) or var(--destructive) fill?
│  └─ ALWAYS var(--primary-foreground) (never var(--foreground)!)
│
└─ Disabled control?
   └─ opacity: 0.5 + cursor: not-allowed (only place opacity carries state)
```

---

## 3. Canonical Component Catalog & Alt Names

Use these canonical roles across artboards so `DESIGN.md`, CSS classes, and handoffs
speak one vocabulary (modeled on Make Kits `components/overview.md`):

| Canonical Role | Alt Names (do not mix in one project) | Structural Rules |
| --- | --- | --- |
| `Button` | CTA, ActionButton, PillButton | `hug contents` (web/desktop) or `fill` (mobile sheet); `gap: 8px` icon↔label; min height 40px (44px mobile) |
| `ButtonGroup` | ActionRow, FormFooter | Uniform button size across every child; `gap: 8px` or `12px`; primary on right |
| `Card` | Panel, Tile, MetricBox | Only when grouping fails without it; padding `24px` web / `16px` mobile / `12–16px` desktop |
| `Field` | InputGroup, FormControl | Explicit `<label>` (`14px` medium) above input; `40–44px` control height; `1px solid var(--input)`; inline error under field |
| `DataTable` | Grid, DenseList | `14px` cells, `32–44px` row height, `tabular-nums`, right-aligned numerics, `1px` row hairlines |
| `StateSwitcher` | ViewStates, ModeToggle | Optional artboard preview strip (`Default / Loading / Empty / Error`) — visually distinct chrome outside the app frame or tucked in a top artboard toolbar |
| `EmptyState` | ZeroState, NoResults | Monochrome icon/line glyph (`40–48px`), 1-line title, 1-line explanation, 1 primary action |
| `Skeleton` | ShimmerPlaceholder | Matches exact final row/card geometry (`var(--muted)`); honors `prefers-reduced-motion` |

---

## 4. `CORRECT / WRONG` Reference Pairs

```html
<!-- WRONG: foreground text on solid primary collides when primary is dark/saturated -->
<button style="background: var(--primary); color: var(--foreground);">Save</button>

<!-- CORRECT: explicit foreground pair guarantees contrast in both light and dark modes -->
<button class="btn btn-primary">Save</button>
<!-- CSS: background: var(--primary); color: var(--primary-foreground); -->
```

```html
<!-- WRONG: mixed button sizes & primary placed left of Cancel -->
<div class="actions">
  <button class="btn btn-primary btn-sm">Publish</button>
  <button class="btn btn-secondary btn-md">Cancel</button>
</div>

<!-- CORRECT: uniform height, Cancel left, primary right -->
<div class="actions">
  <button class="btn btn-secondary btn-md">Cancel</button>
  <button class="btn btn-primary btn-md">Publish</button>
</div>
```

```html
<!-- WRONG: wrapping every nested box in a 1px card border ("box-in-a-box slop") -->
<section class="card">
  <div class="card">
    <div class="card">Metric</div>
  </div>
</section>

<!-- CORRECT: outer region uses spacing/surface step; only the atomic data unit has a hairline -->
<section class="section">
  <div class="grid-3">
    <article class="metric-panel">Metric</article>
  </div>
</section>
```

```html
<!-- WRONG: fading a 20px title to 35% opacity to make it look "secondary" -->
<p style="font-size: 20px; opacity: 0.35;">Updated 4m ago</p>

<!-- CORRECT: step down the type ramp while preserving WCAG AA contrast -->
<p class="meta">Updated 4m ago</p>
<!-- CSS: font-size: 0.75rem; line-height: 1rem; color: var(--muted-foreground); -->
```

```html
<!-- WRONG: raw HTML form fields grouped vertically one per full-width row -->
<form>
  <input placeholder="City" />
  <input placeholder="Postal code" />
</form>

<!-- CORRECT: _example multi-field grouping with visible labels and paired horizontal row -->
<div class="field-row">
  <div class="field">
    <label for="city">City</label>
    <input id="city" type="text" value="Buenos Aires" />
  </div>
  <div class="field field-compact">
    <label for="zip">Postal code</label>
    <input id="zip" type="text" value="C1426" />
  </div>
</div>
```
