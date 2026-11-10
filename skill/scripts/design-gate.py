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

Known limits (a finding is a review prompt, not a verdict; this table is the honest
boundary of a static scan)
---------------------------------------------------------------------------
* Rules R10 (numbered markers) and R9 are conservative and can only flag; the gate
  cannot know whether `01/02/03` is a real sequence or an emoji is meaningful.
* Durations and colors behind `var()` cannot be evaluated statically.
* `width`/`height`/`font-size` literals are *not* checked here — the type and size
  ramps are verified by the checklist items B1/B3, which need semantic intent.
* Selectors are read syntactically; CSS nesting, keyframes and `@media` are handled,
  but `@supports`-style conditional token overrides other than the ones listed above
  are not classified as token blocks.
* Inline `style=""` attributes are scanned for color/radius/transition/spacing rules
  but not for R1/R5/R6/R7, which are file-global.
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
}

#: shadcn/ui semantic roles (token-system.md §1, evidence E1).
SEMANTIC_TOKENS = (
    "background",
    "foreground",
    "card",
    "primary",
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

MAX_TRANSITION_MS = 500

HEX_COLOR_RE = re.compile(
    r"(?<![&\w])#([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})(?![0-9a-fA-F])"
)
FUNC_COLOR_RE = re.compile(r"(?<![\w-])(rgba?|hsla?|hwb|oklch|oklab|lab|lch)\s*\(")
PX_RE = re.compile(r"(?<![\w.-])(-?\d+(?:\.\d+)?)px\b")
DURATION_RE = re.compile(r"(?<![\w.-])(\d+(?:\.\d+)?)(ms|s)\b")
SPACING_PROP_RE = re.compile(r"^(?:margin|padding)(?:-[\w-]+)?$|^(?:row-|column-)?gap$")
TRANSITION_PROP_RE = re.compile(r"^transition(?:-property|-duration)?$")

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

    def _for_each_declaration(self, text, start, end, allow_color):
        """Dispatch every declaration in a leaf body / inline style to the rules."""
        for prop, value, prop_off, value_start, _value_end in parse_declarations(
            text, start, end
        ):
            low = value.lower()
            self._rule_color(value, prop_off, value_start, allow_color)
            self._rule_spacing(prop, value, prop_off)
            self._rule_transition(prop, value, prop_off, low)
            self._rule_radius(prop, value, prop_off)
            self._rule_font(prop, value, prop_off)

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
        """R1 token-block."""
        if self.root_block is None:
            self.add(
                "R1",
                0,
                "no `:root` token block — declare the semantic roles "
                "(" + "/".join(SEMANTIC_TOKENS) + ") before any component CSS (A1)",
            )
            return
        body = self.css_clean[self.root_block["body_start"] : self.root_block["body_end"]]
        declared = {prop for prop, *_ in parse_declarations(body, 0, len(body))}
        for token in SEMANTIC_TOKENS:
            if f"--{token}" not in declared:
                self.add(
                    "R1",
                    self.root_block["body_start"],
                    f"missing semantic token `--{token}` in :root (A1/A2, E1)",
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
            )
        self._rule_inline_and_attributes()
        self._rule_motion()
        self._rule_focus()
        self._rule_icons()
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
            "(12 rules; see references/professional-pass.md)."
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
