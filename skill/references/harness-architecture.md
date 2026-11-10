# How design harnesses work — architecture patterns (reverse-engineered)

Evidence: `evidence.md` §E9. Each pattern names the harnesses that use it (with
sources) and how `gentle-design-skill` + `gentle-design` implement it.

## P1 — Persistent design source-of-truth (DESIGN.md)

**Who**: Google `design.md` spec ("human-readable markdown prose and machine-readable
YAML design tokens"), Stitch projects, Vercel `design.md`, Superdesign, MagicPath
("keeps the Markdown as the system's source").
**Mechanics**: one durable markdown file holds tokens + rationale ("Do's and Don'ts"),
read across sessions so design memory never resets per turn; Vercel measured **57%
fewer design failures** with it (91 → 39 failures in their test).
**Here**: `design/system.md` (gentle-design sync) + the `:root` token block mandated
by the Foundation Pass; per-design `tokens.md` (like Pulse's) freezes the commitment.

## P2 — Pre-code design plan & commitment gate

**Who**: Anthropic `frontend-design` ("Work in two passes. First, brainstorm a short
design plan... create a compact token system"), Stitch `generate-design` (prompt
enhancement before any generation call), Lovable pre-build Design guidance.
**Mechanics**: the agent must resolve audience, direction, and a 4–6 color token plan
BEFORE writing markup — pulling output away from statistical averages.
**Here**: Foundation Pass (fix tokens first) + gentle-design's brief → slug →
directions flow; design.json `tradeoff` per artboard is the written commitment.

## P3 — Explicit anti-slop bans paired with named alternatives

**Who**: Anthropic `web-artifacts-builder` ("avoid using excessive centered layouts,
purple gradients, uniform rounded corners, and Inter font"), Stitch `taste-design`
(encode as explicit "NEVER DO" rules; "No emojis anywhere"), Vercel guidelines.
**Mechanics**: forbid canonical clichés AND name the replacement — a ban without an
alternative just produces a different cliché.
**Here**: `generic-vs-professional.md` (each "Generic" pairs with a "Fix") + anti-slop
section G of the Professional Pass.

## P4 — Constrained vocabulary offloaded from context

**Who**: v0 (shadcn primitives + runtime vector lookup), Vercel `design.md` ("none of
the code enters the model's context"), unverified v0/Lovable leaks ("Everything must
be themed via the design system").
**Mechanics**: the model emits semantic token names, never ad-hoc values; stylesheets
and primitives live outside the context budget.
**Here**: Hard Rule 2 (no ad-hoc hex/px inside component CSS) + Professional Pass A2
(static check).

## P5 — Progressive disclosure of guidance

**Who**: Figma Make kits ("Multiple short guidelines files are better than a few large
files"), v0's dynamic system prompt, Stitch skill routing.
**Mechanics**: a small index routes to granular per-concern files; only relevant
guidance enters context.
**Here**: this skill's own structure — SKILL.md is the index; platform references load
per target (web/mobile/desktop); evidence.md loads only when provenance matters.

## P6 — Deterministic validation gates (lint, contrast, auto-retry)

**Who**: `design.md` linter (11 rules: broken refs, missing primary, WCAG 4.5:1
contrast from converted sRGB, orphaned tokens, section order), v0 AutoFixers (AST
rewrites; v0-1.5-md 93.87% error-free vs 64.71% baseline), Lovable auto-retry ("When
violations are found, Lovable automatically retries to correct them"), Vercel
`web-design-guidelines` audit skill (`file:line` findings).
**Mechanics**: mechanical invariants are checked by code, not judgment; violations
trigger targeted fixes automatically.
**Here**: the Professional Pass as an assertion list (the Pulse verification encoded
it as 86 mechanical checks: token completeness, ramp-only values, computed AA
contrast) — runnable per artboard before reporting done.

## P7 — Externalized render → screenshot → critique → fix loop

**Who**: Anthropic `frontend-design` ("Critique your own work... taking screenshots"),
Stitch `stitch-loop` (download screens "AND visually audited"), Superdesign ("Claude
cannot judge its own output, so you feed it the actual render and demand a concrete
diff"), FieldPacket ("visual verification must come from outside the generating step";
Amazon CITL: up to 17.8% quality gain over three critique cycles).
**Mechanics**: render in a browser, capture pixels, critique against the brief with a
fresh view, fix, re-check — 2–3 bounded iterations.
**Here**: Professional Pass H1 + gentle-design canvas (live render + comments) +
agent-browser screenshots; the Pulse verification found its only real issue (hero
mid-animation) this way.

## P8 — Separate taste exploration from engineering

**Who**: Superdesign `--mode branch` ("forks the design into a new variation instead
of mutating it in place"), Stitch's generate-design → react-components split,
gentle-design's own artboard model.
**Mechanics**: divergent visual exploration happens in disposable artifacts; frozen,
reviewed choices then feed deterministic implementation.
**Here**: gentle-design's "3 clearly different directions" + manifest `Chosen`
artboard → `implement` handoff; iteration edits only the targeted artboard.

## What we deliberately do NOT adopt

- **Mid-stream model surgery** (v0's LLM Suspense / composite models): requires v0's
  serving stack; our equivalent is the capture/critique loop (P7).
- **MCP-gated generation APIs**: gentle-design works from self-contained HTML files
  locally; no external generation service in the loop.
- **Auto-retry without review** (Lovable): bounded by gentle-design's human-in-the-loop
  canvas comments; automated fixes stay within the correction pass.
