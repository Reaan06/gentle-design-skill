---
name: gentle-design-skill
description: "Trigger: designing UI artboards with the gentle-design workflow when the result must look professionally crafted — landing pages, dashboards, product screens, marketing pages. Encodes the design systems of Vercel v0, Google Stitch, and Figma-class AI tools (reverse-engineered with evidence) as mechanical rules: token foundation, type scale, spacing rhythm, color discipline, states, motion, and a final professional pass. Pairs with gentle-design (delivery) and gentle-ui-design (UX quality)."
license: MIT
metadata:
  author: gentleman-programming
  version: "1.2.0"
  evidence: references/evidence.md (REA reverse engineering, v1.1.0)
---

# gentle-design-skill

Professional-grade polish for gentle-design artboards. This skill owns **visual
craft quality** (what makes output look like it came from Vercel v0, Google Stitch,
or a senior product designer); `gentle-design` owns the workflow and delivery, and
`gentle-ui-design` owns UX/usability rules. The three compose: workflow → usability →
craft.

## Activation Contract

Load this skill when producing or reviewing artboards whose goal includes
"professional", "high quality", "polished", "like v0/Stitch/Figma", or when an
artboard looks generic and the user wants it elevated. It applies to all three target
surfaces: **Web** (responsive pages), **Mobile** (app screens), and **Desktop**
(desktop-class applications) — the platform references extend the shared foundation.
Do not use it to implement production code in the project's stack.

## Hard Rules

1. **Evidence over vibes.** Every numeric rule below comes from `references/evidence.md`
   (reverse-engineered from shadcn/ui, Tailwind v4, Radix, and the target tools'
   published output). When deviating deliberately, name the deviation and why.
2. **One system per design.** Before writing any artboard, fix its token block
   (colors, type scale, spacing, radius, shadows) as CSS custom properties in
   `:root` and use only those tokens. No ad-hoc hex values, sizes, or durations
   inside component CSS. (System discovered in shadcn theming; see evidence E1.)
3. **Restraint is the signature.** The professional tools' default is a near-monochrome
   palette where ONE accent (or none) carries meaning, borders are low-contrast gray,
   and surfaces are white/near-black (evidence E1, E2). More than ~2 hue families plus
   a status hue is a defect unless the brief demands a brand palette.
4. **Self-contained artboards.** Same rules as gentle-design: inline everything,
   system font stacks only (or the font stack declared in the design's tokens),
   no external URLs.
5. **Accessibility is not negotiable.** WCAG AA contrast, visible focus, and
   `prefers-reduced-motion` — same contract as gentle-ui-design.

## The Foundation Pass (do this first, every brief)

Fix these before any layout. Values and sources in `references/token-system.md`.

0. **Visual thesis + register.** Fix the six-axis register (density, warmth,
   formality, energy, ornament, contrast) from the product type, then write the
   visual thesis as one sentence. Every later choice must serve it; if the design
   would survive the substitution test (swap name/logo/accent → still plausible for
   another product), the thesis is too weak (see `references/generic-vs-professional.md` §9).

1. **Semantic color roles**, not raw colors: `--background, --foreground, --card,
   --primary, --secondary, --muted, --accent, --destructive, --border, --input,
   --ring`. Dark mode is the same roles, re-mapped — never hard-coded darks.
2. **Type scale** on the documented ramp (12/14/16/18/20/24/30/36/48/60/72 px with
   Tailwind's paired line-heights). Display sizes get `letter-spacing: -0.02em…-0.04em`;
   the tools' landings use 60–72px display headlines (evidence E2).
3. **Spacing rhythm**: 4px base, component paddings on the 8/12/16/24/32/48/64 steps.
   Section padding on landing pages is generous (96–128px vertical) — air is a feature
   (evidence E2).
4. **Radius**: one `--radius` token (0.625rem default) with derived small/large
   variants (`calc(var(--radius) ± 2px/4px)`); `9999px` only for true pills/badges.
5. **Elevation**: shadows are rare and subtle. Prefer a 1px `--border` for structure;
   reserve shadow for genuinely floating layers (dropdowns, modals, cards over color).

## The Craft Pass (during composition)

- **Hierarchy by weight and size, not by color**: one display size, one h-size,
  body at `--muted` gray for secondary text. Never make every line bold. Body measure
  ≤65ch–80ch; max 2 font families; `tabular-nums` on comparing numbers.
- **Restraint & hierarchy**: `--primary` used sparingly (one CTA per view); status hues
  (green/amber/red) only for real status; grays for all structure; surface contrast
  and spacing air before wrapper borders; scale-down before opacity-fade
  (`references/composition-patterns.md`).
- **Texture over decoration**: subtle gradients (radial accent glow, dotted grids,
  1px hairlines) instead of colorful blobs. Stitch's landing: black canvas + faint
  dot grid + single gradient edge (evidence E2).
- **States are designed, not defaulted**: hover (subtle background shift), focus
  (2px `--ring` with offset), active, disabled (reduced opacity + `not-allowed`),
  empty/loading/error per gentle-ui-design's adaptive rules.
- **Motion**: 100–250ms ease-out for micro-transitions, 300–500ms for entrances
  (staggered 40–80ms), pressed feedback ≈scale(0.97); transform/opacity only;
  everything honors `prefers-reduced-motion`.

## The Professional Gate (before reporting an artboard done)

Run both deterministic gates first (see `references/professional-pass.md` §H1):
- Static 21-rule gate: `python3 <this-skill>/scripts/design-gate.py <artboard.html>`
  (regression-pinned by the negative fixture corpus in `fixtures/negative/`, one
  broken artboard per rule `R1`–`R21`)
- Browser visual audit (desktop `1440x900` + mobile `390x844`): `python3 <this-skill>/scripts/visual-audit.py <artboard.html>`

Run every item; fix or justify before finishing using the Traffic-Light Critique
(`ROJO` / `AMARILLO` / `VERDE`) in `references/professional-pass.md`.

1. All colors/sizes/durations resolve to tokens in `:root`.
2. ≤2 hue families + status hues; `--primary` appears on ≤3 elements per view.
3. Type ramp used in order; no skipped steps; display ≤72px with negative tracking.
4. Spacing values only from the 4px ramp; section air ≥96px on landing pages.
5. Every interactive element has hover/focus-visible/active/disabled styles.
6. Contrast ≥4.5:1 body / ≥3:1 large text and UI controls.
7. Empty, loading, and error states exist or are deliberately out of scope (say so).
8. `prefers-reduced-motion` media query present when any animation exists.

## Decision Gates

| Situation | Action |
| --- | --- |
| New brief with gentle-design | Pick a style direction (or dice-deal 2–3) from `references/style-directions.md`, write the Direction Contract, then run Foundation Pass tokens |
| Target is a web page (landing/marketing/dashboard/docs) | Apply `references/platform-web.md` |
| Target is a mobile app screen (phone frame) | Apply `references/platform-mobile.md` (390/412px frame, touch targets ≥44px, one type system named) |
| Target is a desktop-class app (IDE/tool/panes) | Apply `references/platform-desktop.md` (14px chrome, dense rows, keyboard affordances) |
| Mixed/multi-surface brief | Design each surface with its platform reference; share the same token block |
| Artboard looks "generic AI" | Diff against `references/generic-vs-professional.md` and fix the named gaps |
| Brief demands a brand palette | Keep the semantic roles + ramp, map the brand into the roles (Rule 3 exception, named in the artboard tradeoff) |
| Design approved / handed off | Emit `design/<slug>/DESIGN.md` (YAML tokens + rationale per the Google spec) and lint it: `npx -y @google/design.md lint design/<slug>/DESIGN.md` |
| User wants to sync the installed skill copies | Fingerprint the source copy once: `python3 <this-skill>/scripts/sync-check.py manifest <installed-src>` and keep the output as `sync-manifest.json` next to it. Before every sync run `python3 <this-skill>/scripts/sync-check.py verify <installed-src> sync-manifest.json` (exit 0 = unchanged, 1 = drift); `compare <src> <dest>` for a quick two-root diff |
| User wants to tune values | Same as gentle-design: sliders + "Copy as prompt" |

## Output Contract

Return: the token block used (or its diff from the previous artboard), which
Foundation/Craft/Gate items were applied, any deliberate deviations (with the
evidence entry cited), and the gentle-design output contract (slug, artboards,
tradeoffs, canvas URL). When a direction or design is approved, also emit
`design/<slug>/DESIGN.md` (machine-readable tokens + human rationale — the P1
pattern from `references/harness-architecture.md`) and keep it lint-clean.

## References

- `references/evidence.md` — REA evidence log: sources, captures, quotes (read when a rule's origin matters).
- `references/token-system.md` — the concrete token library (colors, type, spacing, radius, shadows) with sources.
- `references/platform-web.md` — web pages: landing, marketing, dashboard, docs, responsive story.
- `references/platform-mobile.md` — mobile app screens: iOS/Material conventions, touch, safe areas, sheets.
- `references/platform-desktop.md` — desktop-class apps: panes, density, keyboard, command palette.
- `references/style-directions.md` — named art-direction catalog (8 directions + Direction Contract) to break convergence before tokens.
- `references/harness-architecture.md` — how AI design harnesses work internally (Stitch, design.md, v0, Anthropic, Lovable) and which patterns this skill adopts.
- `references/dark-mode.md` — first-class dark theme rules (role re-mapping, lightness-ladder elevation, contrast on dark pairs).
- `references/professional-pass.md` — the full pre-delivery checklist (per-platform checks at the end of each platform reference).
- `references/composition-patterns.md` — Make Kits-style decision trees, button frequency & group symmetry, surface-vs-border hierarchy, layout intent, and `CORRECT / WRONG` pairs (E11/E12).
- `references/generic-vs-professional.md` — the named differentiators, with fixes, plus the anti-generic playbook (thesis, register, substitution test, named alternatives).
- `gentle-ui-design` skill — usability and adaptive-interface rules (companion).
