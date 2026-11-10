# Generic vs Professional — named differentiators

Why AI output looks "AI-generated" and what the professional tools do instead.
Sources: `evidence.md` E2–E8.

## 1. Palette convergence

**Generic**: default indigo `#6366F1` → violet `#A855F7` gradient, 5+ hue families,
colored blobs behind the hero.
**Professional**: 3–5 colors total, near-monochrome with one accent (shadcn default is
literally black-on-white); purple only when the brand demands it. Texture — dot grids,
hairlines, one low-alpha radial glow — replaces colorful decoration.

**Fix**: rebuild the palette from semantic roles; cap hues; swap blobs for texture.

## 2. Uniform three-card SaaS grid

**Generic**: centered hero + 3 identical icon cards + footer; every section same shape.
**Professional**: sections differ in structure (some dense, some airy); asymmetric
composition; one focal element carries the boldness, the rest stays quiet.

**Fix**: vary section skeletons; spend boldness in exactly one place.

## 3. Weak typography

**Generic**: Inter at 16–20px everywhere, bold-everything headings, uniform radius.
**Professional**: full ramp used (display at 48–72px, line-height 1, tight negative
tracking); body 16/24 muted-gray secondary; uppercase only as tiny loose-tracked labels.

**Fix**: run the Typography section of the Professional Pass.

## 4. States that don't exist

**Generic**: single default state; hover = default; no focus ring; no empty/error.
**Professional**: "All states designed. Empty, sparse, dense, & error states" (Vercel
guidelines); focus ring always visible; pressed feedback (scale 0.97).

**Fix**: add the full state matrix; declare out-of-scope states explicitly.

## 5. Motion that guessworks

**Generic**: `transition: all .3s`, bouncy spring everything, animated layout properties.
**Professional**: explicit properties only (transform/opacity), 100–250ms micro,
300–500ms entrances staggered 40–80ms, `prefers-reduced-motion` honored.

**Fix**: enumerate transition properties; use the duration tokens.

## 6. Numbers and alignment sloppiness

**Generic**: proportional digits in tables/KPIs, off-by-2px icon alignment.
**Professional**: `tabular-nums` on numbers, ±1px optical alignment discipline.

## 7. Underspecified foundation

**Generic**: ad-hoc values per element (the model re-decides every size each time).
**Professional**: tokens frozen before generation (Stitch: "Do NOT include hex codes…
in a generation prompt" — the theme comes first); ~90% neutral surfaces; brand color
reserved for primary actions.

**Fix**: the Foundation Pass before any layout work.

## 8. No critique loop

**Generic**: first-pass output shipped unchecked.
**Professional**: render → screenshot → critique → fix (visual critic loop).

**Fix**: Pass section H — mandatory before reporting done.

## 9. The anti-generic playbook (T9 research — mechanics that break convergence)

Banning one default is not enough ("Ban Inter and the model converges on Space
Grotesk" — E10). These techniques replace prohibitions with positive commitments.
Apply them in order when a design must not look machine-made:

1. **Visual thesis (one sentence) + six-axis register.** Before tokens: fix the
   register — density (airy↔dense), warmth (cold↔warm), formality (playful↔formal),
   energy (calm↔energetic), ornament (plain↔ornate), contrast (soft↔hard) — from the
   product type, then commit to a one-sentence thesis ("Boarding-pass typography for
   a freight dashboard"). Every later choice must serve the thesis.
2. **Extremes, not midpoints.** Weight jumps 100/200 vs 800/900 (never 400 vs 600);
   size jumps 3x+ (never 1.5x); one dominant color + one sharp accent. The median is
   the slop zone (E10, Claude cookbook).
3. **Named alternatives, never bare bans.** Every NEVER-DO pairs with the chosen
   replacement (banning centered heroes → the chosen asymmetric split). This skill's
   token system IS the named alternative set.
4. **Substitution test (the 80% rule).** If swapping product name, logo, and accent
   color leaves 80% of the page equally plausible for another product, the design is
   generic. Fix: pull one structural or typographic decision from the thesis that
   ONLY fits this product.
5. **Card-necessity rule.** "If removing a border, shadow, background, or radius does
   not hurt interaction or understanding, it should not be a card" (E10). Strips the
   default card-wrapper slop.
6. **Frequency-gated motion.** High-frequency, low-novelty controls (command menus,
   context menus, tabs) skip entry animation entirely; reserve motion for
   first-impression surfaces (E10, rauno.me).
7. **Browser-surface theming.** Style what most AI output forgets: `::selection`,
   caret color, scrollbar, `:focus-visible` ring, underline offset — the finish layer
   that separates craft from template (E10, impeccable).
8. **One structural signature.** Deal candidate structures rather than always ranking
   the same pattern; keep exactly one memorable structural decision per design and
   let the rest be quiet (spend boldness in one place, E8/E10).

Mechanical tells to scan for before delivery (deterministic, E10 design-slop cop):
colored card top/left stripes, badge/eyebrow above H1, Inter/Roboto dominance,
`01 / 02 / 03` markers on non-sequential content, emoji-as-icon, purple gradients,
uniform radii everywhere, all cards identical width.
