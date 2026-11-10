#!/usr/bin/env python3
"""design-gate.py — deterministic mechanical design gate for `gentle-design-skill`.

The skill's Professional Pass (`references/professional-pass.md`) is a checklist for a
human/agent reader. This script makes the mechanical half of it executable: a
deterministic static scan of a self-contained HTML artboard, no browser, no network,
Python 3 standard library only.

Usage
-----
    python3 design-gate.py <artboard.html> [more.html ...] [--json]

Exit codes
----------
    0  clean (no findings)
    1  findings reported
    2  usage error (no files, unknown flag, unreadable file)

Output
------
One line per finding, in the `file:line` shape used by vercel-labs
web-interface-guidelines:

    design/foo.html:42 [R4 transition-all] "transition: all" — ...

`--json` emits one `{"file": ..., "findings": [{"rule", "line", "message"}]}` object
per file; an array of those objects when more than one file is given.
Findings are sorted by line, then rule id — the output is byte-stable for a given
input.

Evidence anchors
----------------
E10 (`references/evidence.md`) is the source for the mechanical tells this gate
scans: adriankrebs.ch "design-slop cop" (deterministic DOM/CSS scoring rather than
screenshot judgement), vercel-labs web-interface-guidelines (`file:line` findings,
"never `transition: all`", "no `outline-none` without `:focus-visible`"),
anthropics/skills frontend-design ("before adding numbered markers, check the content
really is a sequence"), fieldpacket.dev ("named alternatives, not just
prohibitions"), and E1/E7 (shadcn semantic token roles, Tailwind's 4px ramp) for the
token and ramp rules.

Each rule is a mechanical restatement of one Professional Pass item:

    R1  token-block              -> A1, A2   (:root semantic set, E1/E7)
    R2  raw-color-outside-root   -> A2, A3   (tokens-only surfaces)
    R3  off-ramp-spacing         -> D1       (4px ramp)
    R4  transition-all           -> F4       ("never `transition: all`", E10)
    R5  missing-reduced-motion   -> F5
    R6  missing-focus-visible    -> F1       (E10: no `outline-none` without it)
    R7  font-tell                -> A4       (Inter/Roboto-first; named alternatives)
    R8  slop-palette             -> C1, C4   (default indigo/violet gradients)
    R9  emoji-icon               -> G1, G4
    R10 numbered-markers         -> G4       (decorative 01/02/03; review flag)
    R11 radius-drift             -> E1
    R12 transition-duration-tell -> F3       (100-250ms micro-transitions)
    R13 unsafe-on-primary        -> A2, E12  (--primary-foreground / --on-brand pairing)
    R14 wrapper-border-box       -> D, E12   (non-interactive layout wrappers with full box borders)
    R15 micro-text-size          -> B1       (font-size literals < 12px / < 0.75rem)
    R16 media-dimensions-alt     -> F1, G    (<img> alt+dimensions, <svg> width/height)
    R17 root-contrast-pair       -> C3, E12  (static WCAG AA >= 4.5:1 on hex pairs in :root)
    R18 ramp-integrity           -> B1, B3   (font-size off the documented type ramp)
    R19 surface-legibility       -> C5, E2   (text over unverifiable gradient/low-alpha surfaces)
    R20 specificity-tell         -> A2, E10  (more than two `!important` declarations)
    R21 elevation-overshoot      -> E2       (box-shadow blur radius > 40px)

Deliberate allowances (kept narrow so the gate stays quiet on real artboards)
---------------------------------------------------------------------------
* Raw color literals are allowed in `:root`, in token re-map blocks
  (`[data-theme=...]`, `.dark`, `@media (prefers-color-scheme: ...)`) and inside
  `calc()` derivations of tokens — those are the places a token system legitimately
  declares literal color.
* `margin`/`padding`/`gap` declarations are exempt from the ramp rule when the value
  uses `calc()` (a token derivation, not an ad-hoc number). Negative ramp steps
  (`margin: -8px`) are allowed; only the magnitude has to be on the ramp.
* A slop hex inside a `gradient()` is reported once by R8 and not twice by R2.
* `rgb()`/hex inside `mask-image` is still reported: a mask stencil is a literal
  color and belongs in a token too (the fix is one token, not an exception).
* Emoji detection deliberately ignores arrows and technical symbols (`→`, `⌘`, `⇧`,
  `<kbd>` glyphs) — only pictographic ranges count.
* `!important` inside the canonical `@media (prefers-reduced-motion: reduce)` reset is
  exempt from R20: that snippet needs `!important` to beat component transitions and
  is the one place the cascade escape hatch is warranted.
* R19 reads the surface alpha of the *same* selector only (one `var()` hop into
  `:root`). A verifiable solid background on that selector — the `--*-foreground`
  pairing — silences the rule, because the contrast can then be computed.
* R21 measures the blur radius only: `0 0 0 9999px`-style ring/hairline tricks and
  `inset` hairlines keep a blur of `0` and never fire, however large the spread is.

Known limits (a finding is a review prompt, not a verdict; this table is the honest
boundary of a static scan)
---------------------------------------------------------------------------
* Rules R10 (numbered markers) and R9 are conservative and can only flag; the gate
  cannot know whether `01/02/03` is a real sequence or an emoji is meaningful.
* Durations and colors behind `var()` cannot be evaluated statically.
* `width`/`height`/`font-size` rules: `R15` checks explicit `font-size` literals
  below `12px`/`0.75rem`, while `var(--text-*)` indirections and layout sizing remain
  covered by checklist items B1/B3 and `visual-audit.py`.
* `R17` checks literal hex token pairs in `:root` (when `--foreground`/`--muted-foreground`
  /`--primary-foreground`/`--card-foreground` and their backgrounds are hex literals);
  `oklch()`/`lab()` pairs and computed DOM contrast are verified by `visual-audit.py`.
* `R18` resolves `var(--text-*)` and px/rem literals (rem assumes the 16px root);
  `em`, `%`, `ch` and `vw` sizes stay unverified. Heading order is compared only for
  selectors that target a bare `h1`–`h6` tag — class-scoped titles are read by a human.
* `R19` cannot compute a real contrast ratio over a gradient: it reports the pairing
  as unverifiable and leaves the measured value to `visual-audit.py`.
* `R20` counts `!important` occurrences, not their effect on the cascade.
* Selectors are read syntactically; CSS nesting, keyframes and `@media` are handled,
  but `@supports`-style conditional token overrides other than the ones listed above
  are not classified as token blocks.
* Inline `style=""` attributes are scanned for the per-declaration rules (R2-R4, R11,
  R12, R15, R18, R19, R21) and for `!important` (R20); the file-global rules R1, R5, R6
  and R7 read the stylesheet only.
"""

from __future__ import annotations

import argparse
import bisect
import json
import os
import re
import sys

# --------------------------------------------------------------------------- #
# Rule catalogue
# --------------------------------------------------------------------------- #

RULES = {
    "R1": "token-block",
    "R2": "raw-color-outside-root",
    "R3": "off-ramp-spacing",
    "R4": "transition-all",
    "R5": "missing-reduced-motion",
    "R6": "missing-focus-visible",
    "R7": "font-tell",
    "R8": "slop-palette",
    "R9": "emoji-icon",
    "R10": "numbered-markers",
    "R11": "radius-drift",
    "R12": "transition-duration-tell",
    "R13": "unsafe-on-primary",
    "R14": "wrapper-border-box",
    "R15": "micro-text-size",
    "R16": "media-dimensions-alt",
    "R17": "root-contrast-pair",
    "R18": "ramp-integrity",
    "R19": "surface-legibility",
    "R20": "specificity-tell",
    "R21": "elevation-overshoot",
}

#: shadcn/ui semantic roles (token-system.md §1, evidence E1).
SEMANTIC_TOKENS = (
    "background",
    "foreground",
    "card",
    "primary",
    "primary-foreground",
    "secondary",
    "muted",
    "accent",
    "destructive",
    "border",
    "input",
    "ring",
    "radius",
)

#: Tailwind v4 4px ramp steps allowed for spacing (token-system.md §3, E7).
SPACING_RAMP = frozenset({1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128})

#: Default indigo/violet gradient hexes (generic-vs-professional.md §1, E4/E10).
SLOP_HEX = frozenset({"6366f1", "8b5cf6", "a855f7", "7c3aed"})

#: Fonts whose first-position dominance is the canonical AI tell (E10).
TELL_FONTS = frozenset({"inter", "roboto"})

#: Documented type ramp steps (professional-pass.md B1, evidence E7). Steps declared as
#: `--text-*` tokens in the artboard's `:root` extend this set (e.g. 28/44/56).
TEXT_RAMP = frozenset({12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72})

#: Smallest ramp step; anything below it belongs to R15 (micro text).
TEXT_RAMP_MIN = min(TEXT_RAMP)

#: Root font size assumed when a `font-size` is given in `rem`.
ROOT_FONT_PX = 16.0

#: `!important` budget per stylesheet (R20).
MAX_IMPORTANT = 2

#: A background below this alpha cannot carry statically verifiable text (R19).
MIN_BG_ALPHA = 0.25

#: Translucent text over a gradient below this alpha is unverifiable (R19).
MIN_TEXT_ALPHA_ON_GRADIENT = 0.6

#: Blur radius above which elevation reads as a generic drop shadow (R21).
MAX_SHADOW_BLUR_PX = 40.0

MAX_TRANSITION_MS = 500

HEX_COLOR_RE = re.compile(
    r"(?<![&\w])#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})(?![0-9a-fA-F])"
)
FUNC_COLOR_RE = re.compile(r"(?<![\w-])(rgba?|hsla?|hwb|oklch|oklab|lab|lch)\s*\(")
PX_RE = re.compile(r"(?<![\w.-])(-?\d+(?:\.\d+)?)px\b")
DURATION_RE = re.compile(r"(?<![\w.-])(\d+(?:\.\d+)?)(ms|s)\b")
SPACING_PROP_RE = re.compile(r"^(?:margin|padding)(?:-[\w-]+)?$|^(?:row-|column-)?gap$")
TRANSITION_PROP_RE = re.compile(r"^transition(?:-property|-duration)?$")
GRADIENT_RE = re.compile(r"(?:repeating-)?(?:linear|radial|conic)-gradient\s*\(", re.IGNORECASE)
IMPORTANT_RE = re.compile(r"!\s*important\b", re.IGNORECASE)
ALPHA_HEX_RE = re.compile(
    r"(?<![&\w])#([0-9a-fA-F]{4}|[0-9a-fA-F]{8})(?![0-9a-fA-F])"
)
FUNC_COLOR_VALUE_RE = re.compile(
    r"(?<![\w-])(rgba?|hsla?|hwb|oklch|oklab|lab|lch)\s*\(([^()]*)\)"
)
VAR_CALL_RE = re.compile(r"var\(\s*(--[\w-]+)\s*\)")
REDUCED_MOTION_MEDIA_RE = re.compile(r"@media\b[^{]*\{", re.IGNORECASE)

#: Pictographic emoji ranges. Arrows (2190-21FF) and technical symbols (2300-23FF)
#: are excluded on purpose: `→`, `⌘`, `⇧` are typography, not icon slop.
EMOJI_RE = re.compile(
    "[" "\U0001f000-\U0001faff" "\u2600-\u27bf" "\u2b00-\u2bff" "\ufe0f" "\u200d" "]"
)

TAG_RE = re.compile(r"<(/?)([a-zA-Z][\w:-]*)([^>]*?)(/?)>")
VOID_TAGS = frozenset(
    "area base br col embed hr img input link meta param source track wbr".split()
)
INTERACTIVE_TAGS = frozenset({"button", "a", "input", "select", "textarea"})
ICON_HOST_TAGS = frozenset({"button", "a", "nav"})
HEADING_TAGS = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})
MARKER_CLASS_RE = re.compile(r"\b(?:index|idx|num|number|step|marker|badge|count)\b")
NUMBER_MARKER_RE = re.compile(r"^\s*0[1-9](?:[.)]\s|\s*[—–-]\s|\s*[.)]?\s*$)")

DECL_RE = re.compile(r"(?P<prop>--[\w-]+|[-a-zA-Z][\w-]*)\s*:")

#: Markup attributes whose value is a color (SVG/canvas presentation attributes).
COLOR_ATTR_RE = re.compile(
    r"(?<![\w-])(fill|stroke|stop-color|flood-color|lighting-color|color|bgcolor)"
    r"\s*=\s*[\"']([^\"']*)[\"']",
    re.IGNORECASE,
)
STYLE_ATTR_RE = re.compile(r"(?<![\w-])style\s*=\s*[\"']([^\"']*)[\"']", re.IGNORECASE)
LAYOUT_WRAPPER_SEL_RE = re.compile(
    r"(?:^|[\s,>])(?:section|main|header|footer|article|aside"
    r"|\.(?:section|wrapper|container|layout|grid|stack|band|shell|panel-grid|hero-grid))\b",
    re.IGNORECASE,
)
REM_RE = re.compile(r"(?<![\w.-])(-?\d+(?:\.\d+)?)rem\b", re.IGNORECASE)
ATTR_CHECK_RE = re.compile(r"\b(width|height|alt)\s*=", re.IGNORECASE)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
SCRIPT_BLOCK_RE = re.compile(r"<script\b[^>]*>(.*?)</script>", re.IGNORECASE | re.DOTALL)


# --------------------------------------------------------------------------- #
# Text helpers (all length-preserving, so offsets always map back to the source)
# --------------------------------------------------------------------------- #


def blank(chars, start, end):
    """Blank `chars[start:end]`, keeping newlines so every offset stays valid."""
    for i in range(start, min(end, len(chars))):
        if chars[i] != "\n":
            chars[i] = " "


def skip_string(text, i, end):
    """Return the index just past the string literal starting at `i`."""
    quote = text[i]
    i += 1
    while i < end:
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == quote:
            return i + 1
        i += 1
    return end


def split_top(value, sep_chars):
    """Split on separators at paren depth 0 (keeps `rgb(0 0 0 / .1)` intact)."""
    parts, cur, depth = [], [], 0
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if depth == 0 and ch in sep_chars:
            if cur:
                parts.append("".join(cur))
                cur = []
            continue
        cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def enclosing_function(value, index):
    """Name of the function call whose arguments contain `value[index]`, or ``""``."""
    depth = 0
    k = index - 1
    while k >= 0:
        ch = value[k]
        if ch == ")":
            depth += 1
        elif ch == "(":
            if depth == 0:
                m = re.search(r"([-\w]+)$", value[:k])
                return m.group(1).lower() if m else ""
            depth -= 1
        k -= 1
    return ""


def call_excerpt(value, index, limit=32):
    """Readable excerpt of the function call starting at `index` (`rgb(0 0 0)`)."""
    depth = 0
    k = index
    while k < len(value):
        ch = value[k]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                text = re.sub(r"\s+", " ", value[index : k + 1]).strip()
                return text if len(text) <= limit else text[: limit - 1] + "…"
        k += 1
    return re.sub(r"\s+", " ", value[index : index + limit]).strip()


def parse_blocks(text, start, end):
    """Parse CSS-ish blocks in `text[start:end]`.

    Returns dicts: ``{selector, body_start, body_end, depth}``. Strings are skipped,
    so braces inside `content: "}"` do not corrupt the structure.
    """
    blocks = []
    stack = []
    prelude_start = start
    i = start
    while i < end:
        ch = text[i]
        if ch in "\"'":
            i = skip_string(text, i, end)
            continue
        if ch == "{":
            stack.append(
                {
                    "selector": text[prelude_start:i].strip(),
                    "body_start": i + 1,
                    "body_end": end,
                    "depth": len(stack),
                }
            )
            blocks.append(stack[-1])
            i += 1
            prelude_start = i
            continue
        if ch == "}":
            if stack:
                stack.pop()["body_end"] = i
            i += 1
            prelude_start = i
            continue
        if ch == ";":
            i += 1
            prelude_start = i
            continue
        i += 1
    return blocks


def parse_declarations(text, start, end):
    """Yield ``(prop, value, prop_offset, value_start, value_end)`` for a leaf body."""
    out = []
    i = start
    while i < end:
        m = DECL_RE.search(text, i, end)
        if not m:
            break
        if text[i : m.start()].strip():
            i = m.end()
            continue
        value_start = m.end()
        j = value_start
        depth = 0
        while j < end:
            ch = text[j]
            if ch in "\"'":
                j = skip_string(text, j, end)
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif ch == ";" and depth == 0:
                break
            j += 1
        out.append((m.group("prop"), text[value_start:j], m.start(), value_start, j))
        i = j + 1
    return out


# --------------------------------------------------------------------------- #
# The gate
# --------------------------------------------------------------------------- #


class Gate:
    def __init__(self, path, raw):
        self.path = path
        self.raw = raw
        self.line_starts = [0]
        for m in re.finditer("\n", raw):
            self.line_starts.append(m.end())
        self.findings = []
        self.blocks = []
        self.css_spans = []
        self.script_spans = []
        self.allowed_color_spans = []
        self.root_block = None
        self.root_decls = {}
        self._ramp_cache = None
        self.css_clean = raw
        self.markup = raw
        self._prepare()

    # -- offsets -------------------------------------------------------------

    def line_of(self, offset):
        return bisect.bisect_right(self.line_starts, max(0, offset))

    def add(self, rule_id, offset, message):
        self.findings.append(
            {
                "rule": f"{rule_id} {RULES[rule_id]}",
                "line": self.line_of(offset),
                "message": message,
            }
        )

    # -- input preparation ---------------------------------------------------

    def _prepare(self):
        chars = list(self.raw)
        self.css_spans = [
            (m.start(1), m.end(1)) for m in STYLE_BLOCK_RE.finditer(self.raw)
        ]
        self.script_spans = [
            (m.start(1), m.end(1)) for m in SCRIPT_BLOCK_RE.finditer(self.raw)
        ]

        # Markup view: CSS and JS bodies blanked (same length).
        markup_chars = list(chars)
        for start, end in self.css_spans + self.script_spans:
            blank(markup_chars, start, end)
        self.markup = "".join(markup_chars)

        # CSS view: comments blanked (same length) so values can be scanned safely.
        css_chars = list(chars)
        for start, end in self.css_spans:
            for m in re.finditer(r"/\*.*?\*/", self.raw[start:end], re.DOTALL):
                blank(css_chars, start + m.start(), start + m.end())
        self.css_clean = "".join(css_chars)

        for start, end in self.css_spans:
            self.blocks.extend(parse_blocks(self.css_clean, start, end))

        self.root_block = next(
            (b for b in self.blocks if self._normalized(b["selector"]) == ":root"),
            None,
        )
        for block in self.blocks:
            if block is self.root_block or self._is_token_remap(block["selector"]):
                self.allowed_color_spans.append((block["body_start"], block["body_end"]))

        if self.root_block is not None:
            body = self.css_clean[
                self.root_block["body_start"] : self.root_block["body_end"]
            ]
            for prop, value, *_ in parse_declarations(body, 0, len(body)):
                self.root_decls[prop.strip().lower()] = value.strip()

    @staticmethod
    def _normalized(selector):
        return re.sub(r"\s+", " ", selector).strip()

    def _is_token_remap(self, selector):
        sel = self._normalized(selector).lower()
        if not sel:
            return False
        if "[data-theme" in sel or "[data-color-mode" in sel:
            return True
        if re.search(r"(?:^|[,\s>])\.dark\b", sel):
            return True
        return sel.startswith("@media") and "prefers-color-scheme" in sel

    def _color_allowed(self, offset):
        if any(start <= offset < end for start, end in self.allowed_color_spans):
            return True
        return False

    # -- declarations --------------------------------------------------------

    def _for_each_declaration(self, text, start, end, allow_color, selector=""):
        """Dispatch every declaration in a leaf body / inline style to the rules."""
        decls = parse_declarations(text, start, end)
        decl_map = {prop.lower(): value.strip() for prop, value, *_ in decls}
        self._rule_block_pairing(decls, decl_map)
        self._rule_wrapper_border(selector, decls)
        self._rule_surface_legibility(decls, decl_map)
        for prop, value, prop_off, value_start, _value_end in decls:
            low = value.lower()
            self._rule_color(value, prop_off, value_start, allow_color)
            self._rule_spacing(prop, value, prop_off)
            self._rule_transition(prop, value, prop_off, low)
            self._rule_radius(prop, value, prop_off)
            self._rule_font(prop, value, prop_off)
            self._rule_micro_text(prop, value, prop_off)
            self._rule_text_ramp(prop, value, prop_off)
            self._rule_elevation(prop, value, prop_off)

    def _rule_block_pairing(self, decls, decl_map):
        """R13 unsafe-on-primary when var(--primary) bg pairs with var(--foreground)."""
        bg = decl_map.get("background") or decl_map.get("background-color") or ""
        fg = decl_map.get("color", "")
        if "var(--primary)" in bg and "var(--foreground)" in fg:
            prop_off = next(
                (off for p, _v, off, *_ in decls if p.lower() == "color"),
                decls[0][2],
            )
            self.add(
                "R13",
                prop_off,
                "background `var(--primary)` paired with `var(--foreground)` — "
                "use `var(--primary-foreground)` (or `var(--on-brand)`) (E12)",
            )

    def _rule_wrapper_border(self, selector, decls):
        """R14 wrapper-border-box on non-interactive layout wrappers."""
        if not selector or not LAYOUT_WRAPPER_SEL_RE.search(selector):
            return
        for prop, value, prop_off, *_ in decls:
            if prop.lower() != "border":
                continue
            val = value.strip().lower()
            if re.match(r"^(?:0(?:px)?|none|unset|initial)\b", val):
                continue
            self.add(
                "R14",
                prop_off,
                f"full box `border` on layout wrapper `{selector}` — prefer surface "
                f"contrast, spacing, or a single-edge divider (`border-top`/`border-bottom`) (E12)",
            )

    def _rule_micro_text(self, prop, value, prop_off):
        """R15 micro-text-size (< 12px / < 0.75rem)."""
        if prop.lower() != "font-size":
            return
        m_px = PX_RE.search(value)
        if m_px and 0 < float(m_px.group(1)) < 12:
            self.add(
                "R15",
                prop_off,
                f"font-size {m_px.group(0)} < 12px — keep UI text >= 12px (`0.75rem`) for legibility (B1)",
            )
            return
        m_rem = REM_RE.search(value)
        if m_rem and 0 < float(m_rem.group(1)) < 0.75:
            self.add(
                "R15",
                prop_off,
                f"font-size {m_rem.group(0)} < 0.75rem (12px) — keep UI text >= 12px (B1)",
            )

    # ------------------------------------------------------------------ #
    # v1.2.0 semantic rules (R18-R21)
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_alpha_number(text):
        """Alpha from `0.4` / `40%`, or ``None`` when it is not a number."""
        raw = text.strip()
        if not raw:
            return None
        try:
            if raw.endswith("%"):
                return max(0.0, min(1.0, float(raw[:-1]) / 100.0))
            return max(0.0, min(1.0, float(raw)))
        except ValueError:
            return None

    @classmethod
    def _alpha_from_call(cls, name, args):
        """Alpha declared by a color function call, or ``None`` when opaque."""
        if "/" in args:
            return cls._parse_alpha_number(args.rsplit("/", 1)[1])
        parts = [part.strip() for part in args.split(",")]
        if len(parts) == 4 and name in {"rgba", "hsla"}:
            return cls._parse_alpha_number(parts[3])
        return None

    def _alpha_of(self, value, depth=0):
        """Statically known alpha of a color value (``None`` = opaque or unknown).

        One `var()` hop into `:root` is resolved so token-declared washes
        (`--secondary: rgb(255 255 255 / 0.06)`) are seen; anything the gate
        cannot pin down stays ``None`` and is never reported.
        """
        low = value.strip().lower()
        if not low or low in {
            "none",
            "transparent",
            "currentcolor",
            "inherit",
            "initial",
            "unset",
            "revert",
        }:
            return None
        if GRADIENT_RE.search(low) or "url(" in low:
            return None
        hex_alpha = ALPHA_HEX_RE.search(low)
        if hex_alpha:
            return int(hex_alpha.group(1)[-2:], 16) / 255.0
        call = FUNC_COLOR_VALUE_RE.search(low)
        if call:
            return self._alpha_from_call(call.group(1), call.group(2))
        if depth == 0:
            var_call = VAR_CALL_RE.search(low)
            if var_call and var_call.group(1) in self.root_decls:
                return self._alpha_of(self.root_decls[var_call.group(1)], depth=1)
        return None

    def _rule_surface_legibility(self, decls, decl_map):
        """R19 surface-legibility: translucent ink over a surface it cannot be read on.

        Both halves must be unverifiable: a translucent ink (alpha < 0.6) over a
        gradient or over a wash (background alpha < 0.25). An opaque ink on a wash is
        the sanctioned hover/active pattern (dark-mode.md §4) and stays quiet, as does
        any selector that also declares a solid background the pairing can fall back to.
        """
        fg = decl_map.get("color", "")
        if not fg:
            return
        fg_alpha = self._alpha_of(fg)
        if fg_alpha is None or fg_alpha >= MIN_TEXT_ALPHA_ON_GRADIENT:
            return  # opaque or unknown ink: contrast is verifiable, or not statically seen
        backgrounds = [
            decl_map[key]
            for key in ("background", "background-color", "background-image")
            if decl_map.get(key)
        ]
        if not backgrounds:
            return
        offset = next(
            (off for prop, _value, off, *_ in decls if prop.lower() == "color"),
            decls[0][2],
        )
        alphas = [self._alpha_of(bg) for bg in backgrounds]
        # A verifiable solid pairing on the same selector (the `--*-foreground`
        # contract) supplies the fallback the declaration was written against.
        has_solid = any(
            not GRADIENT_RE.search(bg) and (alpha is None or alpha >= MIN_BG_ALPHA)
            for bg, alpha in zip(backgrounds, alphas)
        )
        if has_solid:
            return
        if any(GRADIENT_RE.search(bg) for bg in backgrounds):
            self.add(
                "R19",
                offset,
                f"text at alpha {fg_alpha:.2f} "
                f"(< {MIN_TEXT_ALPHA_ON_GRADIENT:g}) over a gradient background — the "
                f"contrast cannot be verified statically; use an opaque ink or put a "
                f"solid surface behind it (C5, E2)",
            )
            return
        low_bg = next(
            (alpha for alpha in alphas if alpha is not None and alpha < MIN_BG_ALPHA),
            None,
        )
        if low_bg is not None:
            self.add(
                "R19",
                offset,
                f"text at alpha {fg_alpha:.2f} "
                f"(< {MIN_TEXT_ALPHA_ON_GRADIENT:g}) over a background at alpha "
                f"{low_bg:.2f} (< {MIN_BG_ALPHA:g}) — both layers are translucent, so the "
                f"composited contrast cannot be verified; use an opaque ink (C5, E2)",
            )

    def _text_ramp(self):
        """Documented ramp: base scale plus `--text-*` px tokens declared in `:root`."""
        if self._ramp_cache is not None:
            return self._ramp_cache
        ramp = set(TEXT_RAMP)
        for prop, value in self.root_decls.items():
            if not re.fullmatch(r"--text-[\w-]+", prop) or prop.endswith("-lh"):
                continue
            m = PX_RE.search(value)
            if not m:
                continue
            step = float(m.group(1))
            if step.is_integer():
                ramp.add(int(step))
        self._ramp_cache = ramp
        return ramp

    @staticmethod
    def _length_px(value):
        """Resolve a bare length (`17px`, `1.25rem`) to px, or ``None``."""
        bare = re.sub(r"!\s*important", "", value.strip().lower()).strip()
        m_px = PX_RE.fullmatch(bare)
        if m_px:
            return float(m_px.group(1))
        m_rem = REM_RE.fullmatch(bare)
        if m_rem:
            return float(m_rem.group(1)) * ROOT_FONT_PX
        return None

    def _resolve_font_px(self, value):
        """Resolve a `font-size` (`px`/`rem`/`var(--text-*)`) to px, or ``None``."""
        bare = re.sub(r"!\s*important", "", value.strip().lower()).strip()
        if "var(" in bare:
            var_call = VAR_CALL_RE.match(bare)
            if not var_call or var_call.group(1) not in self.root_decls:
                return None
            return self._resolve_font_px(self.root_decls[var_call.group(1)])
        return self._length_px(bare)

    def _rule_text_ramp(self, prop, value, prop_off):
        """R18 ramp-integrity: `font-size` must land on the documented type ramp."""
        if prop.lower() != "font-size":
            return
        bare = re.sub(r"!\s*important", "", value.strip().lower()).strip()
        if not bare or "var(" in bare:
            return
        m_px = PX_RE.search(bare)
        m_rem = REM_RE.search(bare)
        if m_px is None and m_rem is None:
            return  # em/%/ch/vw and keyword sizes are not statically verifiable
        px_values = []
        if m_px is not None:
            px_values.append(float(m_px.group(1)))
        if m_rem is not None:
            px_values.append(float(m_rem.group(1)) * ROOT_FONT_PX)
        if any(px_value < TEXT_RAMP_MIN for px_value in px_values):
            return  # micro text belongs to R15
        ramp = self._text_ramp()
        for px_value in px_values:
            if px_value.is_integer() and int(px_value) in ramp:
                continue
            self.add(
                "R18",
                prop_off,
                f"font-size `{bare}` is off the documented type ramp — use "
                f"`var(--text-*)` or a ramp step (12/14/16/18/20/24/30/36/48/60/72 plus "
                f"the `--text-*` steps declared in :root) (B1, B3)",
            )
            return

    @staticmethod
    def _heading_levels(selector):
        """Heading levels targeted by a bare `h1`-`h6` selector, else an empty set."""
        levels = set()
        for part in split_top(selector, ","):
            tail = re.split(r"[\s>+~]", part.strip())[-1]
            tail = re.sub(r"::?[\w-]+(?:\([^()]*\))?", "", tail)
            m = re.fullmatch(r"h([1-6])", tail.strip())
            if m:
                levels.add(int(m.group(1)))
        return levels

    def _rule_heading_scale(self):
        """R18 ramp-integrity: heading levels must not grow with depth."""
        sizes = {}
        ambiguous = set()
        for block in self.blocks:
            levels = self._heading_levels(block["selector"])
            if not levels:
                continue
            body_start = block["body_start"]
            body = self.css_clean[body_start : block["body_end"]]
            if "{" in body:
                continue
            size = offset = None
            for prop, value, prop_off, *_ in parse_declarations(body, 0, len(body)):
                if prop.lower() != "font-size":
                    continue
                size = self._resolve_font_px(value)
                offset = body_start + prop_off
                break
            if size is None:
                continue
            for level in levels:
                if level in sizes and sizes[level][0] != size:
                    ambiguous.add(level)
                sizes.setdefault(level, (size, offset))
        for level in range(1, 6):
            if level in ambiguous or (level + 1) in ambiguous:
                continue
            if level not in sizes or (level + 1) not in sizes:
                continue
            deeper_size, deeper_offset = sizes[level + 1]
            shallower_size = sizes[level][0]
            if deeper_size > shallower_size:
                self.add(
                    "R18",
                    deeper_offset,
                    f"h{level + 1} font-size {deeper_size:g}px exceeds h{level} "
                    f"{shallower_size:g}px — heading levels must not grow with depth "
                    f"(B1, B3)",
                )

    def _reduced_motion_spans(self):
        """Spans of `@media (prefers-reduced-motion: …)` blocks (R20 allowance)."""
        spans = []
        css = self.css_clean
        for m in REDUCED_MOTION_MEDIA_RE.finditer(css):
            if "prefers-reduced-motion" not in m.group(0).lower():
                continue
            start = m.end() - 1
            depth = 0
            i = start
            while i < len(css):
                ch = css[i]
                if ch in "\"'":
                    i = skip_string(css, i, len(css))
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        spans.append((start, i + 1))
                        break
                i += 1
        return spans

    def _rule_specificity(self):
        """R20 specificity-tell: more than `MAX_IMPORTANT` `!important` declarations."""
        spans = self._reduced_motion_spans()
        count = 0
        first = None
        for start, end in self.css_spans:
            for m in IMPORTANT_RE.finditer(self.css_clean, start, end):
                if any(span_start <= m.start() < span_end for span_start, span_end in spans):
                    continue
                count += 1
                first = m.start() if first is None else first
        for m in STYLE_ATTR_RE.finditer(self.markup):
            for hit in IMPORTANT_RE.finditer(m.group(1)):
                count += 1
                first = m.start(1) + hit.start() if first is None else first
        if count > MAX_IMPORTANT:
            self.add(
                "R20",
                first or 0,
                f"{count} `!important` declarations (budget {MAX_IMPORTANT}) — a "
                f"specificity war is a design smell; scope the selector or fix the token "
                f"layer instead (A2, E10)",
            )

    @staticmethod
    def _shadow_blur(layer):
        """Blur radius of one `box-shadow` layer (0 with fewer than three lengths)."""
        lengths = []
        for token in layer.split():
            if token.lower() == "inset":
                continue
            m_px = PX_RE.fullmatch(token)
            if m_px:
                lengths.append(float(m_px.group(1)))
                continue
            if re.fullmatch(r"[+-]?0(?:\.0+)?", token):
                lengths.append(0.0)
                continue
            break  # shadow grammar: lengths first, then <color>
        return lengths[2] if len(lengths) >= 3 else 0.0

    def _rule_elevation(self, prop, value, prop_off):
        """R21 elevation-overshoot: blur radius > 40px on any `box-shadow` layer."""
        if prop.lower() != "box-shadow":
            return
        for layer in split_top(value, ","):
            blur = self._shadow_blur(layer)
            if blur <= MAX_SHADOW_BLUR_PX:
                continue
            self.add(
                "R21",
                prop_off,
                f"box-shadow blur {blur:g}px > {MAX_SHADOW_BLUR_PX:g}px — professional "
                f"surfaces keep elevation subtle (small blur, alpha <= 0.12); a wide blur "
                f"reads as a generic drop shadow (E2)",
            )
            return

    def _rule_color(self, value, prop_off, value_start, allow_color):
        """R2 raw-color-outside-root (and R8 for gradient slop hexes).

        R8 owns slop hexes inside `gradient()` so a single line is not reported twice.
        """
        if allow_color:
            return
        gradient = "gradient(" in value.lower()
        seen_slop = set()
        for m in HEX_COLOR_RE.finditer(value):
            hex_value = m.group(1).lower()
            abs_off = value_start + m.start()
            if gradient and hex_value in SLOP_HEX:
                seen_slop.add("#" + hex_value)
                continue
            if self._color_allowed(abs_off):
                continue
            if self._calc_token_derivation(value, m.start()):
                continue
            self.add(
                "R2",
                prop_off,
                f'raw color literal "#{hex_value}" outside :root — use a token '
                f"declared in :root (or a [data-theme]/prefers-color-scheme re-map)",
            )
        for m in FUNC_COLOR_RE.finditer(value):
            abs_off = value_start + m.start()
            if self._color_allowed(abs_off):
                continue
            if self._calc_token_derivation(value, m.start()):
                continue
            self.add(
                "R2",
                prop_off,
                f"raw color `{call_excerpt(value, m.start())}` outside :root — use a "
                f"token declared in :root (or a [data-theme]/prefers-color-scheme re-map)",
            )
        if seen_slop:
            self.add(
                "R8",
                prop_off,
                "default indigo/violet gradient "
                + ", ".join(sorted(seen_slop))
                + " — use the design's accent token, or texture instead "
                "(C1/C4, generic-vs-professional.md §1)",
            )

    @staticmethod
    def _calc_token_derivation(value, index):
        """True when the literal sits in a `calc()` that derives from a token."""
        if enclosing_function(value, index) != "calc":
            return False
        return "var(--" in value

    def _rule_spacing(self, prop, value, prop_off):
        """R3 off-ramp-spacing."""
        if not SPACING_PROP_RE.match(prop):
            return
        if "calc(" in value.lower():
            return
        for m in PX_RE.finditer(value):
            magnitude = abs(float(m.group(1)))
            on_ramp = magnitude.is_integer() and int(magnitude) in SPACING_RAMP
            if magnitude == 0 or on_ramp:
                continue
            self.add(
                "R3",
                prop_off,
                f"off-ramp spacing {m.group(0).lstrip('+')} in `{prop}` — use the 4px "
                f"ramp (1,2,4,8,12,16,20,24,32,40,48,64,80,96,128)",
            )

    def _rule_transition(self, prop, value, prop_off, low):
        """R4 transition-all and R12 transition-duration-tell."""
        if not TRANSITION_PROP_RE.match(prop):
            return
        if re.search(r"\ball\b", low):
            self.add(
                "R4",
                prop_off,
                '`transition: all` — enumerate the animated properties '
                "(transform/opacity/color/background-color)",
            )
        for m in DURATION_RE.finditer(value):
            amount = float(m.group(1))
            ms = amount * 1000 if m.group(2) == "s" else amount
            if ms > MAX_TRANSITION_MS:
                self.add(
                    "R12",
                    prop_off,
                    f"transition duration {m.group(0)} > {MAX_TRANSITION_MS}ms — "
                    f"micro-transitions are 100-250ms ease-out (F3)",
                )

    def _rule_radius(self, prop, value, prop_off):
        """R11 radius-drift."""
        if prop.lower() != "border-radius":
            return
        for token in split_top(value, " /"):
            if self._radius_token_ok(token):
                continue
            self.add(
                "R11",
                prop_off,
                f'radius drift "{token}" — use var(--radius*) / '
                f"calc(var(--radius) ± …) / 9999px (E1)",
            )

    @staticmethod
    def _radius_token_ok(token):
        token = token.strip()
        if not token or token in {"0", "normal", "inherit", "initial", "unset"}:
            return True
        if token == "9999px":
            return True
        if token.startswith("var(--radius"):
            return True
        if token.startswith("calc(") and "var(--radius" in token:
            return True
        return False

    def _rule_font(self, prop, value, prop_off):
        """R7 font-tell."""
        low_prop = prop.lower()
        if low_prop != "font-family" and not low_prop.startswith("--font"):
            return
        families = split_top(value, ",")
        if not families:
            return
        first = families[0].strip().strip("\"'“”").strip().lower()
        if first in TELL_FONTS:
            self.add(
                "R7",
                prop_off,
                f'"{families[0].strip()}" is first in `{prop}` — the default AI tell; '
                f"name an alternative that serves the visual thesis "
                f"(system-ui stack or the design's declared face) (E10, A4)",
            )

    # -- file-global rules ---------------------------------------------------

    def _rule_token_block(self):
        """R1 token-block, R13 on-primary role presence, and R17 root hex contrast."""
        if self.root_block is None:
            self.add(
                "R1",
                0,
                "no `:root` token block — declare the semantic roles "
                "(" + "/".join(SEMANTIC_TOKENS) + ") before any component CSS (A1)",
            )
            return
        declared = dict(self.root_decls)
        for token in SEMANTIC_TOKENS:
            if f"--{token}" not in declared:
                if token == "primary-foreground":
                    if "--on-brand" not in declared:
                        self.add(
                            "R13",
                            self.root_block["body_start"],
                            "missing `--primary-foreground` (or `--on-brand`) in :root "
                            "— pair every `--primary` surface with an explicit on-brand ink (E12)",
                        )
                    continue
                self.add(
                    "R1",
                    self.root_block["body_start"],
                    f"missing semantic token `--{token}` in :root (A1/A2, E1)",
                )
        self._check_root_contrast(declared)

    @staticmethod
    def _parse_hex_rgb(val):
        m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", val.strip())
        if not m:
            return None
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def _contrast_ratio(rgb_a, rgb_b):
        def lum(rgb):
            def ch(c):
                s = c / 255.0
                return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

            return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])

        la, lb = lum(rgb_a), lum(rgb_b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    def _check_root_contrast(self, declared):
        """R17 root-contrast-pair on literal hex foreground/background token pairs."""
        pairs = [
            ("--foreground", "--background"),
            ("--muted-foreground", "--background"),
            ("--primary-foreground", "--primary"),
            ("--on-brand", "--primary"),
            ("--card-foreground", "--card"),
        ]
        for fg_tok, bg_tok in pairs:
            if fg_tok not in declared or bg_tok not in declared:
                continue
            fg_rgb = self._parse_hex_rgb(declared[fg_tok])
            bg_rgb = self._parse_hex_rgb(declared[bg_tok])
            if fg_rgb and bg_rgb:
                ratio = self._contrast_ratio(fg_rgb, bg_rgb)
                if ratio < 4.5:
                    self.add(
                        "R17",
                        self.root_block["body_start"],
                        f"`:root` pair `{fg_tok}` on `{bg_tok}` has contrast "
                        f"{ratio:.2f}:1 (< 4.5:1 WCAG AA) (C3, E12)",
                    )

    def _rule_motion(self):
        """R5 missing-reduced-motion."""
        css = self.css_clean
        trigger = re.search(r"@keyframes\b", css, re.IGNORECASE)
        if trigger is None:
            trigger = re.search(r"(?<![\w-])animation(?:-name)?\s*:", css)
        if trigger is None:
            return
        if re.search(r"prefers-reduced-motion", css):
            return
        self.add(
            "R5",
            trigger.start(),
            "@keyframes/animation present but no `@media (prefers-reduced-motion: "
            "reduce)` block (F5)",
        )

    def _rule_focus(self):
        """R6 missing-focus-visible."""
        first_interactive = None
        for m in TAG_RE.finditer(self.markup):
            if m.group(1):
                continue
            name = m.group(2).lower()
            attrs = m.group(3)
            if name in INTERACTIVE_TAGS or re.search(
                r"role\s*=\s*[\"']?button", attrs, re.IGNORECASE
            ):
                first_interactive = m.start()
                break
        if first_interactive is None:
            return
        if re.search(r":focus-visible", self.css_clean):
            return
        self.add(
            "R6",
            first_interactive,
            "interactive elements present but no `:focus-visible` rule — add "
            "`outline: 2px solid var(--ring); outline-offset: 2px` (F1)",
        )

    def _iter_elements(self):
        """Yield ``(tag, attrs, open_end, text, text_offset)`` for paired elements."""
        stack = []
        for m in TAG_RE.finditer(self.markup):
            closing, name, attrs, self_closing = (
                m.group(1),
                m.group(2).lower(),
                m.group(3),
                m.group(4),
            )
            if self_closing or name in VOID_TAGS:
                continue
            if closing:
                for k in range(len(stack) - 1, -1, -1):
                    if stack[k][0] == name:
                        tag, attrs_, open_end = stack[k]
                        del stack[k:]
                        yield tag, attrs_, open_end, self.markup[open_end : m.start()], open_end
                        break
            else:
                stack.append((name, attrs, m.end()))

    def _rule_icons(self):
        """R9 emoji-icon and R10 numbered-markers (both review flags)."""
        for tag, attrs, _open_end, text, text_offset in self._iter_elements():
            if tag in ICON_HOST_TAGS:
                for m in EMOJI_RE.finditer(text):
                    self.add(
                        "R9",
                        text_offset + m.start(),
                        f'emoji "{m.group(0)}" used as icon inside <{tag}> — draw an '
                        f"inline SVG glyph instead (G1/G4, E10)",
                    )
            if not text.strip():
                continue
            if tag in HEADING_TAGS or (
                tag in {"span", "div", "p", "li", "strong", "em"}
                and MARKER_CLASS_RE.search(attrs or "")
            ):
                marker = NUMBER_MARKER_RE.match(text)
                if marker:
                    self.add(
                        "R10",
                        text_offset + marker.start(),
                        f'decorative marker "{marker.group(0).strip()}" near a heading — '
                        f"verify the content is a real sequence (review flag) (G4, E10)",
                    )

    def _rule_inline_and_attributes(self):
        """R2/R3/R4/R11/R12 over inline `style=""` and color-bearing attributes."""
        for m in STYLE_ATTR_RE.finditer(self.markup):
            self._for_each_declaration(
                self.markup, m.start(1), m.end(1), allow_color=False
            )
        for m in COLOR_ATTR_RE.finditer(self.markup):
            attr, value = m.group(1).lower(), m.group(2)
            value_start = m.start(2)
            for cm in HEX_COLOR_RE.finditer(value):
                if self._color_allowed(value_start + cm.start()):
                    continue
                self.add(
                    "R2",
                    m.start(),
                    f'raw color literal "#{cm.group(1).lower()}" in `{attr}=""` — use '
                    f"var(--token) (A2)",
                )
            for cm in FUNC_COLOR_RE.finditer(value):
                if self._color_allowed(value_start + cm.start()):
                    continue
                self.add(
                    "R2",
                    m.start(),
                    f'raw color `{call_excerpt(value, cm.start())}` in `{attr}=""` — use '
                    f"var(--token) (A2)",
                )

    def _rule_media_tags(self):
        """R16 media-dimensions-alt on <img> and <svg> elements."""
        for m in TAG_RE.finditer(self.markup):
            if m.group(1):
                continue
            name = m.group(2).lower()
            attrs = m.group(3) or ""
            found = {a.lower() for a in ATTR_CHECK_RE.findall(attrs)}
            if name == "img":
                missing = [req for req in ("alt", "width", "height") if req not in found]
                if missing:
                    self.add(
                        "R16",
                        m.start(),
                        f"<img> missing {', '.join(missing)} attribute(s) — set explicit dimensions and alt text (F1)",
                    )
            elif name == "svg":
                missing = [req for req in ("width", "height") if req not in found]
                if missing:
                    self.add(
                        "R16",
                        m.start(),
                        f"<svg> missing {', '.join(missing)} attribute(s) — declare explicit pixel dimensions to avoid layout shift (F1)",
                    )

    # -- driver --------------------------------------------------------------

    def run(self):
        self._rule_token_block()
        for block in self.blocks:
            body = self.css_clean[block["body_start"] : block["body_end"]]
            if "{" in body:
                continue  # nested rules are visited as their own blocks
            self._for_each_declaration(
                self.css_clean,
                block["body_start"],
                block["body_end"],
                allow_color=self._is_token_remap(block["selector"])
                or block is self.root_block,
                selector=self._normalized(block["selector"]),
            )
        self._rule_inline_and_attributes()
        self._rule_motion()
        self._rule_focus()
        self._rule_icons()
        self._rule_media_tags()
        self._rule_heading_scale()
        self._rule_specificity()
        return self._sorted_findings()

    def _sorted_findings(self):
        unique = {}
        for finding in self.findings:
            key = (finding["line"], int(finding["rule"].split()[0][1:]))
            unique.setdefault(key, []).append(finding)
        ordered = []
        for key in sorted(unique):
            ordered.extend(unique[key])
        return ordered


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def format_human(path, findings):
    return [f'{path}:{f["line"]} [{f["rule"]}] {f["message"]}' for f in findings]


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="design-gate.py",
        description=(
            "Deterministic mechanical design gate for gentle-design-skill artboards "
            "(21 rules; see references/professional-pass.md)."
        ),
        epilog="Exit codes: 0 clean, 1 findings, 2 usage error.",
    )
    parser.add_argument("files", nargs="*", metavar="artboard.html")
    parser.add_argument(
        "--json",
        action="store_true",
        help='emit {"file": ..., "findings": [{"rule", "line", "message"}]}',
    )
    args = parser.parse_args(argv)

    if not args.files:
        parser.error("no artboard files given")

    reports = []
    for path in args.files:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                raw = handle.read()
        except OSError as exc:
            print(f"design-gate: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        reports.append((path, Gate(path, raw).run()))

    if args.json:
        payload = [
            {"file": os.path.normpath(path), "findings": findings}
            for path, findings in reports
        ]
        document = payload[0] if len(payload) == 1 else payload
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        for path, findings in reports:
            for line in format_human(path, findings):
                print(line)

    return 1 if any(findings for _path, findings in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
