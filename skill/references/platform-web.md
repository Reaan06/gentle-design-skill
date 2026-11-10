# Platform: Web (responsive pages — landing, marketing, dashboard, app shell)

Evidence refs → `evidence.md`. Default artboard width 1440px (gentle-design manifest);
also provide a 390px mobile story when the brief is responsive.

## 1. Landing / marketing pages

**Skeleton variety beats templates** (anti-slop 2): never the same section shape twice.

| Section | Pattern | Spacing (vertical) |
| --- | --- | --- |
| Nav | 64–72px bar, 1px bottom hairline or none; logo left, 4–6 links, one `--primary` CTA | fixed |
| Hero | Display 60–72px `line-height:1`, tracking −0.03em; sub at `lg`/`xl` muted; one CTA (primary) + one ghost; optional product visual or texture | 128 top / 96 bottom |
| Social proof | Logo row at 40–50% opacity, `text-sm`, no cards | 64 |
| Feature blocks | ALTERNATE structures: 2-col split, bento grid, full-bleed stat band — never 3 identical cards | 96 between |
| Metrics | `tabular-nums`, display 48–60px, one line of `sm` muted context | 96 |
| Testimonial | One large quote (`2xl`, measure ≤60ch), attribution `sm`; avatar only if real | 96 |
| CTA band | Highest contrast moment of the page: near-black band on light canvas (or inverse), single action | 96/128 |
| Footer | `text-sm` muted, 4 columns max, 1px top hairline | 64 |

- Hero air is the signature: ≥96–128px vertical padding (E2 captures).
- One texture max per page (dot grid / glow / hairline grid) at ≤6% alpha.
- Max content width: `max-width: 1120–1200px` centered; text blocks ≤65ch.

## 2. Dashboards / data-heavy app shells

- **Shell**: left sidebar 240–264px (`sm` labels), topbar 56–64px, content padding 24–32.
  Sidebar on `--background` (or `--card` tone) separated by 1px `--border` — never
  heavy gray fill.
- **Density**: data views `text-sm` (14px) rows at 40–44px height; controls `text-sm`;
  KPI numbers display-size with `tabular-nums` (E3, E8).
- **Cards**: `--card` surface + 1px `--border` + `--radius-lg`; padding 24; section
  gaps 24. KPI row: 3–4 cards max, each number + delta (green/red only if real status).
- **Tables**: header `text-xs` muted uppercase? NO — use `text-xs` normal-case medium
  weight; row hover wash (`--accent`); numeric columns right-aligned with tabular
  figures; 1px row separators at 50% of `--border` strength.
- **Forms**: labels `text-sm` medium above fields (placeholder never the label);
  fields 40–44px tall, `--radius-md`, `--input` border, focus `--ring` 2px offset 2px.
- **States** (E3 "all states designed"): table empty state = icon + one-line message
  + primary action; loading = skeleton blocks matching final layout (never spinners
  in tables); error = inline banner on `--destructive`-tinted surface with retry.

## 3. Content / docs pages

- Single column ≤72ch, `text-base` 16/24 (docs can drop to 15px); headings from the
  ramp with anchor spacing (h2 32px top margin).
- Sidebar TOC `text-sm` muted, active item foreground + 2px `--primary` left bar.
- Code blocks: near-black on light (or true dark block), `font-mono` `text-sm`,
  `--radius-md`, 1px border.

## 4. Responsive story (when the brief demands it)

- Breakpoints: 1280 / 1024 / 768 / 480. Design the 1440 and 390 stories; let CSS
  `clamp()`/grid auto-fill handle between.
- 768–: sidebar → hamburger into sheet; KPI row 4→2×2; feature split → stacked with
  visual first; nav links → menu button + single CTA.
- 480–: hero display steps down the ramp (72→48→36); touch targets ≥44px; paddings
  16–24; remove decorative texture before removing content.
- Never hide decision-critical data at any width (gentle-ui-design adaptive rule).

## 5. Web artboard self-check (platform-specific)

- [ ] Section skeletons vary; no repeated 3-card rows without cause.
- [ ] Hero ≥96px air; display ≤72px with negative tracking.
- [ ] One CTA per view uses `--primary`; rest ghost/secondary.
- [ ] Data views: 14px rows, 40–44px height, tabular numbers, right-aligned numerics.
- [ ] Empty/loading/error designed for the page's primary data surface.
- [ ] 390px story exists for responsive briefs; nothing decision-critical hidden.
