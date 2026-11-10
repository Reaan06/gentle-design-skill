# Molino — token block

## Direction Contract (frozen — copied from `direction.md`)

> # Direction Contract — Molino (dirección: Editorial / Print)
>
> Autor: el Gentleman (decisión de gusto, pre-tokens — estilo-del-skill §Direction Contract).
>
> - **THESIS**: Una revista de café que además vende el café.
> - **OWN-WORLD**: El taller de un tostador de barrio: papel kraft, tinta de imprenta,
>   sellos de origen, báscula de latón.
> - **STORY**: "Elegí mi molienda y mi frecuencia; el café llega el jueves, fresco,
>   con la nota de cata impresa en la etiqueta."
> - **FIRST VIEWPORT**: Titular serif enorme a la izquierda ("Café del jueves."),
>   sobre columna de texto a 65ch; a la derecha, la "etiqueta" del tueste de la
>   semana como placa impresa (origen, altitud, notas de cata) — una sola
>   composición, sin carrusel.
> - **FORM**: Papel `#FAF7F2`, tinta `#1A1815`, acento oxblood `#7F1D1D` (usado ≤3
>   veces: CTA suscribirse, precio, sello). `--radius: 0.125rem` (casi recto;
>   pill solo para el sello de origen). Densidad: aireada, secciones 96–128px.
>   Ratio de neutralidad ~95%.
> - **FINISH**: Hairlines 1px tinta al 60%; sin sombras; textura de grano de papel
>   ≤3% opcional; motion: fades 300–400ms, nada rebota; sin gradientes.
>
> Anti-convergencia: prohibido en esta dirección — cards con sombra, pilles
> redondeados, gradientes, centrado-todo, iconos emoji. La sustitución debe fallar:
> el language de "etiqueta impresa / folio" solo pertenece a un tostador editorial.

The contract is frozen. Every later choice serves it; if a choice contradicts it, the
choice changes, not the contract. Deviations are recorded in §9.

## The block

Copy-identical in `01-tienda.html` and `02-suscripcion.html` (verified byte-equal).
Source of the model: shadcn/ui semantic roles (evidence E1), the documented Tailwind
paired type ramp and `--spacing: 0.25rem` (E7), Radix derived-step logic (E7), Figma
Make's "~90% neutral surfaces, brand used sparingly" (E6).

```css
:root {
  /* Paper, ink, one red. Roles only — no component ever names a raw color. */
  --background: #faf7f2;            /* paper */
  --foreground: #1a1815;            /* printing ink */
  --card: #faf7f2;                  /* the sheet itself: no card ever gets its own fill */
  --card-foreground: #1a1815;
  --popover: #faf7f2;
  --popover-foreground: #1a1815;
  --primary: #7f1d1d;               /* oxblood — spent exactly three times per view */
  --primary-foreground: #faf7f2;
  --primary-hover: #6a1818;         /* oxblood pressed: 8% ink mixed in, not opacity */
  --secondary: #f2ede4;             /* kraft wash: bands, skeletons, quiet surfaces */
  --secondary-foreground: #1a1815;
  --muted: #f2ede4;
  --muted-foreground: #5f574d;      /* captions, secondary text */
  --accent: #ebe4d8;                /* hover wash, one step under kraft */
  --accent-foreground: #1a1815;
  --destructive: #7f1d1d;           /* same red ink: this system owns one color */
  --destructive-foreground: #faf7f2;
  --border: rgb(26 24 21 / 0.6);    /* the 1px rule: ink at 60% (FINISH) */
  --border-faint: rgb(26 24 21 / 0.2); /* row rules inside the index and the plate */
  --input: rgb(26 24 21 / 0.6);     /* field and ballot boundaries: same ink weight */
  --ring: #1a1815;                  /* focus is ink, never red: red is budgeted */

  /* Radius: near-straight, one token + derivatives (FORM) */
  --radius: 0.125rem;
  --radius-sm: calc(var(--radius) - 1px);
  --radius-md: var(--radius);
  --radius-lg: calc(var(--radius) + 2px);
  --radius-pill: 9999px;            /* the origin stamp, and nothing else */

  /* Type: one serif for the page, one grotesque for printed labels (2 families) */
  --font-serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --font-label: "Helvetica Neue", Helvetica, Arial, sans-serif;
  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --text-xs: 12px;   --text-xs-lh: 16px;
  --text-sm: 14px;   --text-sm-lh: 20px;
  --text-base: 16px; --text-base-lh: 24px;
  --text-lg: 18px;   --text-lg-lh: 28px;
  --text-xl: 20px;   --text-xl-lh: 28px;
  --text-2xl: 24px;  --text-2xl-lh: 32px;
  --text-3xl: 30px;  --text-3xl-lh: 36px;
  --text-4xl: 36px;  --text-4xl-lh: 40px;
  --text-5xl: 48px;  --text-5xl-lh: 1;
  --text-6xl: 60px;  --text-6xl-lh: 1;
  --text-7xl: 72px;  --text-7xl-lh: 1;
  --tracking-display: -0.03em;
  --tracking-tight: -0.015em;
  --tracking-normal: 0;
  --tracking-label: 0.14em;         /* small-caps labels, loose (B6) */
  --tracking-label-tight: 0.1em;     /* the second label weight: wordmark, prices, ballot notes */
  --measure: 65ch;
  --measure-narrow: 52ch;

  /* Spacing: the 4px ramp only (D1) */
  --space-1: 1px;   --space-2: 2px;   --space-4: 4px;   --space-8: 8px;
  --space-12: 12px; --space-16: 16px; --space-20: 20px; --space-24: 24px;
  --space-32: 32px; --space-40: 40px; --space-48: 48px; --space-64: 64px;
  --space-80: 80px; --space-96: 96px; --space-128: 128px;

  /* Layout */
  --container-max: 1248px;
  --plate-w: 420px;
  --summary-w: 416px;
  --board-w: 1440px;
  --board-h: 900px;

  /* Motion: fades only, 300–400ms (FINISH); micro-states stay at 180ms */
  --duration-hover: 180ms;
  --duration-fade: 360ms;
  --stagger: 60ms;
  --ease-out: cubic-bezier(0.2, 0.8, 0.25, 1);
}
```

## 1. Color — 3 hues, 5 declared colors, semantic roles only

| Role | Value | Use | Measured contrast |
| --- | --- | --- | --- |
| `--background` `--card` | `#faf7f2` | paper canvas and every surface. Nothing gets its own fill — plates separate by rule, never by fill (card-necessity rule) | — |
| `--foreground` | `#1a1815` | all display, body and rule-adjacent text | 16.58:1 on paper |
| `--muted-foreground` | `#5f574d` | captions, folio numbers, secondary lines, quiet labels | 6.65:1 on paper · 6.09:1 on kraft · 5.62:1 on hover wash |
| `--primary` | `#7f1d1d` | oxblood: the weekly price, the origin stamp, the subscription CTA — three spends per view, never a fourth | 9.38:1 on paper; paper on it 9.38:1 |
| `--secondary` `--muted` | `#f2ede4` | kraft wash: skeleton bars, quiet plate heads, the form's pressed wash | ink 15.19:1 on it |
| `--accent` | `#ebe4d8` | hover wash only, never a resting surface | ink 14.02:1 on it |
| `--border` | `rgb(26 24 21 / 0.6)` | the printed 1px rule — section rules, plate edges, form groups | 4.54:1 composited (a rule, not text) |
| `--border-faint` | `rgb(26 24 21 / 0.2)` | row rules inside the index and the plate: a lighter letterpress weight | 1.53:1 — structural only, never carries text |
| `--input` | `rgb(26 24 21 / 0.6)` | field underlines and ballot boxes. In a printed form the boundary is the same ink as the rule | 4.54:1 — clears WCAG 1.4.11's 3:1 |
| `--ring` | `#1a1815` | `:focus-visible` outline, 2px + 2px offset. Ink, because red is spent | 16.58:1 |
| `--destructive` | `#7f1d1d` | the summary plate's real error state (board 02 only) — the third and last red spend there | 9.38:1 on paper |

Neutrality: the paper, ink and kraft families cover every surface and every rule; the
only chroma on either board is oxblood, in at most three elements per view. That is
~95% neutral by construction, not by estimate.

## 2. Type — one serif page, one grotesque label

- `--font-serif` (Georgia-class) sets display, headings, coffee names, prose and the
  tasting note. Georgia's old-style figures are the reason **prices are not set in
  serif**: the ramp's tabular requirement (B5) needs lining tabular figures, and a
  price list must align down the column.
- `--font-label` (Helvetica-class grotesque) sets only 12px small-caps metadata: nav,
  column heads, field labels, folio numbers, prices and the stamp. Two families total
  (A4); neither is Inter nor Roboto (E10 tells).
- Display 72/1 with `-0.03em`: the h1 breaks as "Café del / jueves." so the break is
  part of the composition, not a wrap accident. H2 36/40 and the section title 30/36
  carry the rest; body 16/24; standfirst 20/28; labels 12/16 tracked `+0.14em`.
- Prose measure `65ch` (`--measure`), narrow measure `52ch` for the plate's notes.
- Three weights only: 400 serif, 500 labels, 600 never used — a printed page gets its
  hierarchy from size and rule, not from emboldening everything.

## 3. Spacing & layout

4px ramp only, named by pixel value: 1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80,
96, 128. No 28, 36, 44 or 56 exists in this system — Molino does not need a 56px app
bar, so no off-ramp step is required or allowed. Section air is 96px (the contract's
96–128 range, at its tight end because the page is read as a magazine spread, not a
hero billboard). Container 1248px centred in the 1440 board (96px outer margins) with
32px inner padding → a 1184px column that starts at 128px and ends at 1312px.
The hero is `minmax(0, 1fr) 420px` with a 96px gutter; the subscription page is
`minmax(0, 1fr) 416px` with a 96px gutter.

## 4. Radius

`--radius: 0.125rem` (2px) with `--radius-sm: 1px`, `--radius-lg: 4px` and
`--radius-pill: 9999px`. The pill appears once: the round origin stamp. Buttons, the
plate, fields, ballot boxes and rows use `--radius-sm`/`--radius-md`/`0`. A pill on a
rectangular control is a bug in this direction.

## 5. Elevation

No shadow token exists in this system. Depth is a rule: 60% ink for structure, 20% ink
for row separators, and the paper itself for everything else. `box-shadow` appears
nowhere; the only inset effects are the ballot marks, drawn with `background`. This is
the contract's "sin sombras" made mechanical.

## 6. Motion

- `--duration-fade: 360ms` entrance fades (contract: 300–400ms), pure `opacity` —
  nothing translates, nothing bounces. Stagger `--stagger: 60ms` across masthead, hero
  and plate.
- `--duration-hover: 180ms` for color/border/background micro-states (skill ramp
  100–250ms). Only `opacity`, `color`, `background-color`, `border-color` and
  `transform` are ever enumerated; never `transition: all`.
- `:active` press feedback `scale(0.97)` on buttons; `prefers-reduced-motion: reduce`
  flattens every duration and delay to 1ms in both boards.
- No animation runs on the form controls, per frequency-gated motion (E10): a ballot
  is a high-frequency control, so only its color state changes.

## 7. Texture

The contract allows an optional paper grain ≤3%. It is **omitted**: the only ways to
render grain here are a gradient stack or an SVG filter, and the contract forbids
gradients. The paper is flat; the rules and the typography carry the print character.

## 8. What the palette refuses

No shadow, no gradient, no card fill, no second accent, no pill except the stamp, no
emoji icon, no centered hero. Each refusal has a named replacement in the system: a
60% ink rule replaces the shadow, the kraft wash replaces the tinted card, the serif
display replaces the decorative illustration, and the folio number replaces the badge.

## 9. Declared deviations

1. **`--border` and `--input` are the same value.** Pulse separates them because a
   control boundary owes more contrast than a hairline; in a printed form the field
   rule *is* the rule. Both already clear 3:1 (4.54:1 composited), so the separation
   would buy nothing.
2. **`--destructive` equals `--primary`.** The direction owns exactly one chroma, so
   red means both "buy" and "wrong". The test is the spend: 02 has three reds total
   (total, CTA, error label) and 01 has three (weekly price, stamp, subscription CTA).
3. **No grain texture**, see §7.
4. **No dark re-map.** The contract is paper; an inverted twin would be a different
   own-world (kraft under ink), not the same design. Declared out of scope for this
   brief rather than improvised.
5. **`--radius-lg` (4px) is declared and unspent.** It exists so a future floating
   layer cannot invent a fifth radius; no artboard uses it.
6. **The 390 story is not designed.** The brief is one 1440×900 board per page; both
   boards do collapse cleanly (verified: no horizontal overflow at 1024 and 390), but
   no 390 artboard is claimed.
