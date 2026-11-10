# Style directions — named art-direction catalog

Purpose: break distributional convergence BEFORE tokens exist (E8, E10). For a new
brief, pick (or seed with the dice rule below) ONE direction, write its thesis, then
run the Foundation Pass with that bias. Mixing two directions is allowed only with a
dominant/subordinate split (state it in the tradeoff).

Seed rule (impeccable, E10): deal 2–3 candidate directions at random instead of always
reaching for the same safe one; the brief's product type may veto, not rank.

Each direction: thesis pattern, palette bias (seed hexes; still capped at 3–5 colors),
type bias (system stacks only — gentle-design hard rule), structure, texture, motion,
best for, and its characteristic tells to avoid.

## 1. Swiss / Engineering (v0's own register)

- Thesis: "Instrument-panel clarity: the data is the decoration."
- Palette: white/black + 1 functional accent (teal `#0F766E`, blue `#1D4ED8`, green `#15803D`). Near-zero chroma elsewhere.
- Type: `system-ui`/Helvetica-class; heavy weight jumps (400↔700+), tight display tracking, tabular-nums everywhere.
- Structure: strict grid, hairline rules, left-aligned, dense tables, no rounding beyond `--radius-sm`.
- Texture: none, or 1px grid lines only. Motion: 120–180ms opacity/transform only.
- Best for: analytics, devtools, finance, docs. Tells: gradients, big radii, playful illustrations.

## 2. Editorial / Print

- Thesis: "A magazine wrote this page."
- Palette: warm paper `#FAF7F2` + ink `#1A1815` + one editorial accent (oxblood `#7F1D1D`, forest `#14532D`).
- Type: serif stack (`Georgia, 'Times New Roman', serif`) display + body; 65ch measure, generous leading, large pull-quotes.
- Structure: asymmetrical two-column, wide margins, baseline rhythm, numbered folios.
- Texture: hairline rules, generous whitespace; images treated as captioned plates.
- Motion: minimal, 200ms; page feels printed. Best for: content, portfolios, essays, luxury. Tells: card grids, badge spam, centered everything.

## 3. Brutalist / Raw

- Thesis: "The interface shows its bones."
- Palette: 2 colors — `#FFFFFF` + `#000000` + one shock accent used once (`#FF3E00`).
- Type: monospace or system at extreme sizes; uppercase, exposed hierarchy.
- Structure: visible 2px black borders, hard edges (`--radius: 0`), native-looking controls, raw tables.
- Texture: none; whitespace is the texture. Motion: near-zero, instant state changes.
- Best for: indie tools, portfolios, statements, dev communities. Tells: sneaking in soft shadows or rounded pills — that's not brutalism.

## 4. Terminal / Monospace dev

- Thesis: "A shell that happens to have a GUI."
- Palette: near-black `#0A0E14` + green/amber foreground (`#4ADE80`, `#FBBF24`) + one status red; grayscale chrome.
- Type: `ui-monospace, 'Cascadia Code', Menlo, monospace` for EVERYTHING; size carries hierarchy, never weight.
- Structure: panes with 1px borders, status bars, prompt-style labels (`$`, `❯`), keyboard hints everywhere.
- Texture: scanline or dot grid ≤4% alpha. Motion: instant; cursor blink is the only animation.
- Best for: CLI web UIs, infra, log viewers, hacker tools. Tells: proportional fonts in chrome, colorful gradients.

## 5. Soft SaaS / Calm product

- Thesis: "Quiet confidence; the product relaxes the user."
- Palette: light gray canvas `#F6F7F9`, white surfaces, foreground `#111827`, one muted accent (indigo-gray `#4F5D75`, sage `#5B7C6C`).
- Type: system sans, medium weights, ramp strictly per token-system.md.
- Structure: `--radius-lg` cards, 24px paddings, 1px borders (NOT shadows), 32px section gaps.
- Texture: subtle radial wash behind hero (≤6% alpha). Motion: 180–250ms ease-out.
- Best for: B2B products, dashboards, onboarding. Tells: THIS is the median AI look — it must earn neutrality via the substitution test (§9.4); skip unless genuinely enterprise.

## 6. Luxury / Restrained serif

- Thesis: "Fewer, larger, slower."
- Palette: ivory `#F5F2EC` + charcoal `#171512` + gold/bronze `#9A7B4F` accent used ≤3 times.
- Type: serif display (Georgia-class) + light sans body; display 72px+, wide letter-spacing on labels.
- Structure: centered editorial symmetry, 128px+ section air, thin hairlines, no cards — content floats on canvas.
- Texture: single grain/noise ≤3%. Motion: 400–500ms fades, stagger 80ms; nothing bounces.
- Best for: fashion, hospitality, high-end services. Tells: busy grids, bright CTAs, rounded buttons everywhere.

## 7. Playful / Toy-like (use with restraint)

- Thesis: "Serious product, friendly hands."
- Palette: cream `#FFFDF5` + 2 saturated toy primaries (`#2563EB`, `#F59E0B`, `#10B981`) — cap at 3 hues total.
- Type: system sans heavy weights, big radii (`--radius-xl`+), chunky 2px borders.
- Structure: rounded cards, sticker-like badges (max 2 per view), rotated accents ≤2deg.
- Texture: dotted grids, squiggles at low alpha. Motion: spring 250–350ms entrance only.
- Best for: education, kids, consumer apps. Tells: emoji spam, everything rotated, rainbow palettes.

## 8. Dark Glass / Premium dark

- Thesis: "Deep space with lit glass."
- Palette: layered blacks (`#0B0D12` → `#11141B` → `#181C26`) + text at 0.92–0.97 lightness + one luminous accent (cyan `#22D3EE`; violet only if brand demands).
- Type: system sans; hierarchy by lightness steps (not random grays), tight display tracking.
- Structure: translucent surfaces (white 4–8% alpha) + 1px light-alpha borders; elevation = lightness steps, never shadows.
- Texture: one glow (radial, ≤10%) or dot grid ≤6%; halve texture alpha vs light (dark-mode rule).
- Motion: 200–300ms; glow pulses only on live status. Best for: dev tools (dark default), media, fintech night. Tells: purple-blue gradients, neon soup, low-contrast gray text (<4.5:1).

## Direction Contract (write before tokens — impeccable, E10)

One block per design, in the design folder (`design/<slug>/direction.md` or the
`tokens.md` header): `THESIS` (one sentence) · `OWN-WORLD` (the physical/logical place
this UI inhabits) · `STORY` (the user's one-sentence success moment) · `FIRST VIEWPORT`
(the single above-the-fold composition) · `FORM` (seed hexes + radius + density bias) ·
`FINISH` (texture + motion bias). If a later choice contradicts the contract, change
the choice, not the contract.
