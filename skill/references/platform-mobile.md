# Platform: Mobile (390px-first app screens — iOS + Android conventions)

Evidence refs → `evidence.md`. Mobile artboards are phone frames: default manifest
390×844 (iPhone-class) or 412×915 (Android-class). Stitch targets mobile+web with
Material 3 token expansion (E5); this reference encodes those conventions for
self-contained HTML.

## 1. Foundations

- **Spacing**: same 4px ramp; screen margins 16–20px; card padding 16; list row
  height 56–64px (iOS list 44px minimum).
- **Type**: body 16/24 minimum (never below 14); iOS-like ramp: Large Title 34/41
  bold (−0.02em), Title 22/28, Headline 17/24 semibold, Body 17/24, Footnote 13/18,
  Caption 12/16. Material-like ramp: Display 57, Headline 28–32, Title 22, Body 16,
  Label 14. Pick ONE system per design and name it in the tradeoff.
- **Radius**: large surfaces 16–24 (`--radius-xl` and up); buttons/cards `--radius-lg`;
  bottom sheets top-corners 20–28. Full-round pills for primary actions on Android-style.
- **Color**: same semantic roles as web; dark mode is first-class on mobile (design
  both stories when the brief allows).
- **Elevation**: Material levels 0–3 for cards/sheets/FAB; iOS uses blur surfaces
  (`backdrop-filter: blur(20px)` + 60–80% alpha) for bars — one convention per design.

## 2. Structure & navigation patterns

| Pattern | Use | Rules |
| --- | --- | --- |
| Top app bar | scrolled content context | 56px (M3) / 44–52px (iOS); title 22/28; actions ≤3 icons 44×44 |
| Bottom tab bar | ≤5 top-level destinations | height 56 (M3) / 49+safe-area (iOS); active tab: label + filled icon or pill; inactive muted |
| FAB / primary action | single main create action | 56px, `--radius-lg` or full; bottom-right, 16px margins, above tab bar 16px |
| Bottom sheet | filters, details, pickers | drag handle 32×4 at 30% alpha; top radius 24; content max-height 80% scroll |
| List rows | settings, inbox, search results | 56–64px; leading avatar/icon 40, title 16 medium, trailing meta `sm` muted or chevron |
| Segmented control | 2–4 view switches | full pill track on muted surface; active segment card surface + border |
| Pull header / large title | scroll collapse (static artboard: show both states or note it) | Large title 34 collapses to centered 17 |

- **Thumb zone**: primary actions and tab bar live in the bottom half; destructive or
  rare actions top corners; nothing interactive in the top 44px except nav.
- **Safe areas**: artboards visually respect notch (top ≥47px) and home indicator
  (bottom ≥34px) — represent with padding, annotate in a comment if needed.

## 3. Touch & state rules

- Minimum tap target **44×44px** (E8; WCAG 2.2 AA floor 24px, iOS/Android guidance 44/48);
  icon buttons render 40px glyph inside 44–48px hit area.
- `:active`/pressed states are mandatory on mobile (scale 0.97 or 8–12% bg wash, 100ms).
- Ripple (M3-style) OR highlight (iOS-style) — pick one language per design.
- Focus-visible styles only matter for attached keyboards; keep for a11y anyway.
- Haptics/motion: entrances 300–400ms ease-out; sheet slide-up 400ms with 40ms staggered
  content; all under `prefers-reduced-motion`.

## 4. Mobile-specific states (E3 "all states designed")

- Empty screens: centered illustration/texture 120–160px, one line `lg`, one line `sm`
  muted, one primary button — vertically centered in remaining space.
- Loading: skeleton rows matching final list geometry; pull-to-refresh affordance note.
- Error/offline: full-screen variant with retry; inline variant for lists.
- Permission/first-run: explain value before the OS dialog (static note or pre-dialog
  screen).

## 5. Mobile artboard self-check (platform-specific)

- [ ] One type system named (iOS-like or M3-like); body ≥16, labels ≥12.
- [ ] Tab bar ≤5 items; FAB (if any) doesn't collide with it; thumb-zone respected.
- [ ] All touch targets ≥44px with visible pressed states.
- [ ] Safe-area padding represented; bottom sheet radius 24+ if present.
- [ ] Empty/loading/error for the screen's primary content, or declared out of scope.
- [ ] Dark-mode story present or justified.
