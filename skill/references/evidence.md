# Evidence Log (REA reverse engineering, v1)

Method: REA-style evidence discipline — every claim distinguishes **capture** (runtime
observation), **source** (cited official documentation), or **leak/unverified**
(third-party mirror; treated as a hint, never as authority). Collected 2026-11-10.

## E1 — Runtime capture: shadcn/ui default theme (ui.shadcn.com)

Captured live with browser automation (`agent-browser`, Chrome 157, computed styles):

- Semantic tokens on `:root`: `background`/`foreground` (white/near-black),
  `card`=background, `primary`=near-black, `secondary`=`muted`=`accent`=`lab(96.52%)`,
  `destructive`=red, `border`=`input`=`lab(90.95%)`, `ring`=`lab(66.13%)`,
  `--radius: .625rem`, `--font-sans: Geist`.
- Body text: `16px/24px`.
- Interpretation: the default professional engine is **near-monochrome** — the accent
  is the foreground itself; structure comes from 1px gray borders, not shadows or fill.

## E2 — Runtime capture: v0 and Stitch landings (screenshots, 2026-11-10)

- `v0.app` (redirected to /templates): white canvas, ~64px display headline with tight
  tracking, gray 1px-border cards, search as single bordered input, generous vertical
  air (~120px hero section).
- `stitch.withgoogle.com`: near-black canvas, faint dot-grid texture, single huge white
  display headline (~72px), one gradient-edge input card, one pill CTA. No other color.
- Interpretation: both tools' own surfaces practice **restraint**: 1 hue family max,
  texture over decoration, display typography as the hero element.

## E3 — Source: Vercel v0 official guidance

- vercel.com/blog/ai-powered-prototyping-with-design-systems — v0 defaults to shadcn/ui
  "because it's designed with the right primitives and patterns to help models generate
  real, brand-aligned interfaces". Prompt structure: Product surface, Context of use,
  Constraints & taste.
- vercel.com/design/guidelines (official Vercel design system):
  - "All states designed. Empty, sparse, dense, & error states."
  - "Never `transition: all`. Explicitly list only the properties you intend to animate
    (typically `opacity`, `transform`)." GPU-only motion.
  - Optical ±1px alignment, `tabular-nums` for numbers.

## E4 — Leak/unverified: v0 system prompt mirrors (treat as hints only)

Third-party mirrors (github.com/x1xhlol/system-prompts-and-models-of-ai-tools; EliFuzz
awesome-system-prompts). Not official; used as corroborating hints, consistent with E1–E3:

- "ALWAYS use exactly 3-5 colors total." (1 primary brand + 2–3 neutrals + 1–2 accents)
- "ALWAYS limit to maximum 2 font families total."
- No prominent purple/violet unless requested; gradients limited to 2–3 analogous stops.
- Body ≥14px, line-height 1.4–1.6; flexbox before grid; `gap-*` over `space-*`; no
  emojis as icons.

## E5 — Source: Google Stitch

- stitch.withgoogle.com/llms.txt + discuss.ai.google.dev (Stitch Prompt Guide): prompts
  structured as **Anatomy** (layout) / **Vibe** (aesthetic adjectives) / **Content**
  (data); "For complex apps, start high-level and then drill down on details screen by
  screen." Generation = 1–5 variants, default **3**, varying LAYOUT, COLOR_SCHEME,
  IMAGES, TEXT_FONT, TEXT_CONTENT.
- google-labs-code/stitch-skills + google-labs-code/design.md: design tokens live in a
  separate theme (`colorMode`, headline/body/label fonts, `roundness` scale 4/8/12/full,
  seed color + `colorVariant`), expanded to Material-3 named colors. Generation prompts
  must NOT contain hex codes or token values — tokens are frozen first, then screens are
  generated. `DESIGN.md` combines YAML tokens with rationale and is linted for WCAG AA
  (4.5:1).

## E6 — Source: Figma Make / Figma AI

- figma.com/blog/designer-framework-for-better-ai-prompts: TC-EBC prompting (Task,
  Context, Elements, Behavior, Constraints).
- developers.figma.com/docs/code/write-design-system-guidelines (Make Kits):
  ~90% neutral surfaces; brand color "used sparingly for primary actions, active states,
  and small accents only"; surface-color hierarchy over borders; "Multiple short
  guidelines files are better than a few large files" (progressive disclosure).

## E7 — Source: scales

- tailwindcss.com/docs/theme: `--spacing: 0.25rem` (4px); radius xs 2px … 4xl 32px.
- tailwindcss.com/docs/font-size: text-xs 12/16 … text-base 16/24 … text-5xl 48/1 …
  text-9xl 128/1 (line-height 1 above 48px).
- radix-ui.com/colors/docs/palette-composition/understanding-the-scale: 12-step scale —
  1–2 app backgrounds, 3–5 component bg rest/hover/active, 6–8 borders/focus,
  9–10 solid rest/hover, 11–12 low/high-contrast text (APCA Lc 60/90 guaranteed).
- ui.shadcn.com/docs/theming: semantic surface/foreground pairs; `--radius: 0.625rem`
  with derived variants.

## E8 — Analysis: why generic AI UI happens (secondary sources, corroborated)

- superdesign.dev/blog/why-ai-design-looks-generic; fieldpacket.dev/packets/agent-web-design.html:
  "distributional convergence" — underspecified prompts regress to the statistical
  median: Inter + indigo/purple gradients, centered hero + 3 identical icon cards,
  uniform radii, ALL-CAPS eyebrow labels, `01 / 02 / 03` markers.
- anthropics/skills frontend-design SKILL.md: plan 4–6 hex tokens before writing;
  "Spend your boldness in one place. Let one element be the memorable thing, keep
  everything around it quiet and disciplined."
- emilkowal.ski/ui/agents-with-taste: UI durations <300ms (100–250ms micro), reveals
  from `scale(0.95)`, `:active` `scale(0.97)`, body measure `65ch`, `tabular-nums`,
  loose tracking on uppercase, 44px minimum tap targets.
- Render → screenshot → critique loop before delivery (same sources + frontend-design
  SKILL.md).

## Unknowns / limits

- v0's real system prompt is not officially published; E4 mirrors may be outdated.
- Stitch docs page (stitch.withgoogle.com/docs/learn/overview) blocked automated
  extraction; E5 relies on llms.txt, official Google Labs repos, and community guide.
- Figma Agent output internals are undocumented; E6 covered Make Kits overview,
  while E11–E12 extend it with live Figma product captures and full Make Kits + Agent
  docs. `figma.com/community/explore` returned CDN error ("request could not be
  satisfied") during automated capture and remains excluded.

## E9 — Design harness architectures (official sources, 2026-11-10)

How AI design harnesses work internally (full mapping: `harness-architecture.md`):

- Google Stitch skills (github.com/google-labs-code/stitch-skills): generation vs
  build vs utilities skills; "do NOT include any color, font, or theme instructions in
  the generation prompt" once tokens are applied; `.stitch/next-prompt.md` relay baton;
  "GATE: Phase 1 is complete ONLY when all screens have been downloaded ... AND
  visually audited"; `taste-design` encodes "NEVER DO" rules.
- Google design.md (github.com/google-labs-code/design.md): tokens (YAML) + rationale
  prose; linter with 11 rules incl. WCAG AA 4.5:1 contrast from converted sRGB,
  broken refs, orphaned tokens.
- Anthropic skills (github.com/anthropics/skills): frontend-design two-pass ("brainstorm
  a short design plan ... compact token system"; "Critique your own work as you build,
  taking screenshots"); web-artifacts-builder bans "excessive centered layouts, purple
  gradients, uniform rounded corners, and Inter font".
- Vercel v0 architecture (vercel.com/blog/how-we-made-v0-an-effective-coding-agent,
  /v0-composite-model-family): dynamic system prompt + "LLM Suspense" streaming
  rewrites + deterministic/model autofixers (v0-1.5-md 93.87% error-free vs 64.71%);
  design.md pages had "57% fewer" failures (39 vs 91).
- Lovable (docs.lovable.dev): pre-build design guidance questions; "When violations
  are found, Lovable automatically retries to correct them".
- Figma Make kits: "Multiple short guidelines files are better than a few large files."
- Superdesign (superdesign.dev): "--mode branch ... forks the design into a new
  variation instead of mutating it in place"; "Claude cannot judge its own output, so
  you feed it the actual render and demand a concrete diff".
- FieldPacket agent-web-design: "visual verification must come from outside the
  generating step"; Amazon CITL up to 17.8% quality gain over three critique cycles.
- Unverified leaks (x1xhlol repo): Lovable/v0 mandate token-only styling and
  "NEVER exceed 5 total colors without explicit user permission" — hints only.

## E10 — Anti-generic design skills & techniques (T9, mixed-source)

Public skills and guides whose explicit goal is output that does not look like
"vibe coding". Primary sources verified unless marked otherwise:

- anthropics/skills frontend-design: "Before adding numbered markers, check the
  content really is a sequence." (decorative `01/02/03` is a tell)
- superdesigndev/superdesign-skill: hard init gate — no generation until six
  `.superdesign/init/` context files exist.
- Leonxlnx/taste-skill: mechanical Stop-hook gate (`gate.mjs`) running headless
  Chrome across 1440/1024/768/390/320px with a 3-round fix loop.
- Ferousco-dev/anti-slop-design: six-axis register (density, warmth, formality,
  energy, ornament, contrast) + "Write the visual thesis as one sentence before
  writing any code."
- claudiusararu/unslop-ui-skill: "Define each interaction and component style ONCE
  - a shared class or token - and reuse it."
- waybarrios ai-slop skill: substitution test — "could the product name, logo, and
  accent color be swapped while 80% of the page stays equally plausible for another
  product?"
- superdesign.dev: "separate the creative thinking from the implementation"; render
  diff loop — "pasting the real render and forcing a line-by-line diff is the only
  reliable bridge".
- fieldpacket.dev: "Ban Inter and the model converges on Space Grotesk ... The fix
  is named alternatives, not just prohibitions"; computed-style numeric feedback via
  `page.evaluate()`.
- emilkowal.ski/ui/agents-with-taste: deterministic motion flowchart, <300ms,
  `:active` scale(0.97), 65ch measure, tabular-nums, real `…` character, underline
  only for links.
- pbakaus/impeccable: randomized candidate dealing (dice pick 3 structures, breaking
  ranking ruts); 6-block Direction Contract (THESIS/OWN-WORLD/STORY/FIRST
  VIEWPORT/FORM+seed/FINISH); dual isolated critique agents; browser-surface theming
  (selection, caret, scrollbars, focus rings).
- platform.claude.com cookbook `<frontend_aesthetics>`: "Use extremes: 100/200 weight
  vs 800/900, not 400 vs 600. Size jumps of 3x+, not 1.5x."; dominant + sharp-accent
  palettes.
- developers.openai.com GPT-5.4 frontend guide: mood-board anchoring; one composition
  per first viewport; "If removing a border, shadow, background, or radius does not
  hurt interaction or understanding, it should not be a card."
- adriankrebs.ch design-slop cop: deterministic DOM/CSS slop scoring ("I intentionally
  do not take screenshots and let the LLM judge them") — tells: colored card top/left
  stripes, Inter dominance, badge above H1.
- vercel-labs web-interface-guidelines: `file:line` findings; never `transition: all`;
  no `outline-none` without `:focus-visible`; `min-w-0` on truncating flex.
- linear.app/now/how-we-redesigned-the-linear-ui: "instead of having to define 98
  specific variables for each theme, we defined three: base color, accent color, and
  contrast" (LCH-derived).
- rauno.me/craft/interaction-design: frequency-gated motion — high-frequency,
  low-novelty controls (command menus) skip entry animation.
- vercel.com/font: matched multi-axis family (Geist) with equal x-heights across
  Sans/Mono/Serif.
- boring.design: JS-rendered page, content not verifiable (excluded).

## E11 — Runtime capture: Figma live web surfaces (`figma.com/make/`, `/design/`, `/sites/`)

Captured live with `agent-browser` (Chrome headless DOM & computed-style inspection) across
Figma's own marketing and product surfaces:

- **`figma.com/make/`** (`capture`): pure white section canvas (`rgb(255, 255, 255)`,
  `border-width: 0px`), consistent `80px` vertical section padding; font stack
  `figmaSans` (`SF Pro Display`, `system-ui`, `helvetica`, `sans-serif`) + `figmaMono`.
  Dominant measured scale: `18px/25.2px` weight `330` (275 instances — comfortable lead/body
  copy), `16px/22.4px` weight `400` (22), `30px/36px` tracking `-0.66px` weight `400` (19),
  `16px/23.2px` weight `400` (16), `44px/48.4px` tracking `-0.66px` weight `400` (10),
  `16px/20.8px` tracking `+0.64px` weight `400` (5 — uppercase/tracked labels). Monochrome
  black/white base + subtle neutral wash (`oklch(0 0 none / 0.04)`) and sparing accents
  (`rgb(203, 159, 210)` lilac, `rgb(210, 217, 226)` slate).
- **`figma.com/design/`** (`capture`): H1 `44px/48.4px` (`-0.66px`, `weight 400`); dominant
  scale `18px/25.2px` w330 (129), `16px/22.4px` w400 (92), `16px/23.2px` w320 (83),
  `30px/36px` w400 (32), `44px/48.4px` w400 (7). Measured `bordersVsSurfaces` ratio:
  `{bordered: 1, shadowed: 1, surfaceCards: 0}` — hierarchy via whitespace, typography, and
  surface contrast rather than card-border grids. Radii clustered sharply at `2px` (31),
  `9999px` (16), `4px` (15), `8px` (9), `24px` (8).
- **`figma.com/sites/`** (`capture`): high-contrast monochrome CTAs (`rgb(0,0,0)` bg +
  `rgb(255,255,255)` text, `46px` height, `8px` radius, `16–18px` font) paired with
  crisp `3px solid #000` editorial blocks (`24px 32px` padding, `0px` radius).
- **Interpretation**: Figma's own web surfaces avoid the generic `16px` + `1px bordered card`
  grid trap. They keep canvases stark white, tighten display tracking (`-0.015em` to
  `-0.02em`), rely on `16–18px` breathable copy with light/regular weights (`320–400`),
  reserve borders for deliberate editorial framing or interactive controls, and spend
  pastel/brand accents in tiny, isolated moments.

## E12 — Source: Figma Make Kits guidelines & Figma Agent best practices

Extracted from official Figma documentation (`developers.figma.com/docs/code/write-design-system-guidelines`,
`help.figma.com/hc/en-us/articles/38978644498199`, `figma.com/blog/how-to-put-your-design-system-to-work-with-the-figma-agent/`):

1. **Composition over naked atoms**: Help Center explicitly states atomic buttons/inputs
   alone "are difficult for AI to compose into coherent layouts on their own"; AI needs
   higher-order reusable blocks (`Card/OrderSummary/Default`, headers, feature rows) that
   encode Auto Layout intent (`fill container`, `hug contents`, `fixed sizing`, min/max widths).
2. **Decision trees & variant budgets**: Make Kits `button.md` and `color.md` use ASCII
   decision trees for every ambiguous choice (background, text, border, button variant,
   type class), annotate frequency weights (`primary` ~30% one per section / `neutral` ~50%
   default / `subtle` ~20%), and explicitly ban invalid variant names (`Do NOT use "secondary",
   "ghost", "destructive", or "link"` when closed to 3 variants).
3. **Group symmetry & action placement**: `ButtonGroup` rule — all buttons in one group share
   the exact same size variant (never mix `medium` and `small`), and primary CTA sits on the
   right (`Cancel` left, `Save` right).
4. **Surface contrast before borders**: Make Kits `color.md` border decision tree states:
   "Layout region boundary? → No border — use surface color contrast instead (Exception:
   `SidebarNavigation` uses `border-r`)". Borders belong on interactive controls (`input`,
   `select`, clickable card), not every layout wrapper.
5. **Scale before opacity**: Make Kits typography rule: "Reduce importance through scale
   (smaller type class), not opacity" — shrink type step while keeping readable text contrast
   instead of washing out large labels into unreadable low-alpha gray.
6. **Explicit `on-*` contrast pairing**: Make Kits mandates `--on-brand` / `--on-reverse`
   alongside `--brand-primary`, showing `CORRECT` vs `WRONG` pairs (`bg-brand-primary +
   text-on-brand` vs `bg-brand-primary + text-text-primary` where dark text vanishes).
7. **Semantic naming & context taxonomy**: Slash-grouped names (`Button/Primary/Large`,
   `color/surface/primary`), `Examples` / `_example` frames for multi-field form grouping,
   progressive disclosure across short modular `.md` files with `Alt names` synonym tables
   and concrete `CORRECT / WRONG` snippets rather than vague prose ("Do not use small text
   for anything except captions" beats "Use small text sparingly").
