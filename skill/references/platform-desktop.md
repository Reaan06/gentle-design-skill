# Platform: Desktop (desktop-class applications — IDEs, tools, dense productivity UIs)

Evidence refs → `evidence.md`. Desktop app artboards default to 1440×900 or 1280×800.
Desktop is where **density** is a feature and keyboard is a first-class input.

## 1. Foundations

- **Density**: base text 14px (`text-sm`) for UI chrome, 16px for content/reading
  surfaces; row heights 32–36px (lists/tables), 40px for primary controls; padding
  12–16 inside panels, 8 between related controls. Compare web's 24 — desktop is
  tighter by intent (gentle-ui-design density rule: match task frequency/consequence).
- **Type**: same semantic ramp but chrome stays at `sm`; section headers 13–14 medium
  uppercase? No — normal case, muted; document titles 20–24. Monospace for anything
  code/ID/numeric-grid (`tabular-nums`).
- **Radius**: tighter than web — `--radius-md` (6–8px) for controls, `--radius-lg`
  for panels; pills only for status badges. IDE-class tools run 4–6px.
- **Color**: near-monochrome plus syntax/accent layer; panel separation via 1px
  `--border`, active pane via 2px `--primary` edge or `--accent` wash. Dark theme is
  the default story for dev tools (design light as the alternate).

## 2. Structure patterns

| Pattern | Rules |
| --- | --- |
| Activity bar / rail | 48px icon rail, active indicator 2px left bar; tooltips for all |
| Sidebar tree | 240–280px; rows 28–32px; indent 16px/level; hover wash; selected = `--accent` bg + medium weight; context chevrons |
| Multi-pane / split | Panes separated by 1px `--border` (never shadows); resizable handle 4px hover-highlight; active pane titled 12–13px muted |
| Tabbed editor | Tabs 36–40px; active tab = card surface + top 2px `--primary` or no chrome (IDE minimal); modified dot, close on hover |
| Status bar | 24–28px, `text-xs` muted, right-aligned actions; never carries primary actions |
| Command palette | Overlay 640px wide, top 20%; input 44px; rows 36–40px with kbd hints; type-ahead filter state; empty state "No results" |
| Menus / dropdowns | Item height 32px; separators hairline; shortcut hints right in `font-mono text-xs` muted; destructive item in `--destructive` |
| Inspector / properties | Label:value two-column grid; label `text-xs` muted right-aligned; grouped 16px apart with hairlines |

## 3. Keyboard & interaction (desktop's differentiator)

- **Focus order visible**: `:focus-visible` ring everywhere; arrow-key affordances
  suggested for lists/trees (document them in an annotation when static).
- **Shortcuts**: every repeated action gets one; render as `<kbd>`-style chips
  (1px border, `--radius-sm`, `font-mono text-xs`, muted).
- Hover states on ALL chrome (desktop users hover constantly): 8% `--accent` wash,
  100ms.
- Double-click/resize/drag affordances: show grips (6px dots, hairlines) in at least
  one representative state.
- Tooltips: 300ms delay convention; dark `--foreground`/`--background` inverse chip,
  `--radius-sm`, `text-xs`.

## 4. Dense-data states (E3)

- Tables: 32px rows, sticky header with 1px bottom border, right-aligned numerics,
  column sort indicators (▲▼ at 60% alpha), row selection via checkbox column 32px.
- Virtualized-list look: 10–20 visible rows minimum; empty state compact (icon+line,
  not full-screen).
- Loading: skeleton rows at exact final geometry; progress on long ops in status bar.
- Error: inline per-row (trailing `--destructive` icon + tooltip) for item failures;
  banner for pane failures; toast (bottom-right, 360px) for background operations.

## 5. Desktop artboard self-check (platform-specific)

- [ ] Chrome at 14px; row heights 32–36; density matches task frequency.
- [ ] Panes separate via 1px borders, zero decorative shadows; active pane indicated.
- [ ] Shortcuts rendered for ≥3 repeated actions; command palette (if present) has
      input + filtered + empty states.
- [ ] Hover on all chrome; focus-visible ring everywhere.
- [ ] Table/list: sticky header, sort indicator, numeric alignment, compact empty state.
- [ ] Dark theme default for dev tools (light alternate or justified).
