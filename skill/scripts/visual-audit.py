#!/usr/bin/env python3
"""visual-audit.py — browser-backed visual audit for `gentle-design-skill`.

Uses `agent-browser` (headless Chromium) to verify dynamic layout and contrast properties
that static HTML scanning (`design-gate.py`) cannot observe:

1. Desktop (`1440x900`) and Mobile (`390x844`) horizontal overflow (`scrollWidth > innerWidth`).
2. Clipped visible text containers (`scrollWidth > clientWidth + 2` or `scrollHeight > clientHeight + 2`
   with `overflow` clipping).
3. Computed WCAG AA contrast (`>= 4.5:1` normal text, `>= 3.0:1` large text `>= 24px` or bold `>= 18.66px`)
   walking ancestor backgrounds with alpha compositing.
4. Optional viewport screenshots (`--screenshot-dir`).
5. Fixed-desktop artboards are detected deterministically first via
   `<body data-platform="desktop">`; the `.app` computed-style heuristic
   (width >= 1200px with `overflow: hidden`) remains as a fallback for
   unmarked boards. In `--viewport auto` mode the mobile pass is skipped
   for fixed-desktop boards; `--viewport both` (CI mode) always audits both.

Usage
-----
    python3 visual-audit.py <artboard.html> [more.html ...] [--json] [--screenshot-dir DIR]

Exit codes
----------
    0  clean (no blockers)
    1  visual blockers reported
    2  usage or environment error (e.g. missing agent-browser)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("mobile", 390, 844),
]

AUDIT_JS = r"""(() => {
  const parseRgba = (str) => {
    if (!str) return null;
    const m = str.match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+%?))?\s*\)/i);
    if (!m) return null;
    let a = 1;
    if (m[4] !== undefined) {
      a = m[4].endsWith('%') ? parseFloat(m[4]) / 100 : parseFloat(m[4]);
    }
    return { r: parseFloat(m[1]), g: parseFloat(m[2]), b: parseFloat(m[3]), a };
  };
  const composite = (fg, bg) => {
    const a = fg.a + bg.a * (1 - fg.a);
    if (a === 0) return { r: 255, g: 255, b: 255, a: 1 };
    return {
      r: (fg.r * fg.a + bg.r * bg.a * (1 - fg.a)) / a,
      g: (fg.g * fg.a + bg.g * bg.a * (1 - fg.a)) / a,
      b: (fg.b * fg.a + bg.b * bg.a * (1 - fg.a)) / a,
      a,
    };
  };
  const lum = (c) => {
    const ch = (v) => {
      const s = v / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * ch(c.r) + 0.7152 * ch(c.g) + 0.0722 * ch(c.b);
  };
  const ratio = (a, b) => {
    const la = lum(a), lb = lum(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  };
  const resolveBg = (el) => {
    const layers = [];
    let cur = el;
    while (cur && cur.nodeType === 1) {
      const bg = parseRgba(getComputedStyle(cur).backgroundColor);
      if (bg && bg.a > 0) layers.push(bg);
      cur = cur.parentElement;
    }
    let acc = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = layers.length - 1; i >= 0; i--) {
      acc = composite(layers[i], acc);
    }
    return acc;
  };
  const isVisible = (el) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  };

  const docEl = document.documentElement;
  const overflowX = Math.max(0, Math.round(docEl.scrollWidth - window.innerWidth));
  const contrastFailures = [];
  const clippedElements = [];
  let checkedTextNodes = 0;

  const walker = document.createTreeWalker(document.body || docEl, NodeFilter.SHOW_ELEMENT);
  let node;
  while ((node = walker.nextNode())) {
    if (!isVisible(node)) continue;
    if (node.closest('[aria-hidden="true"]')) continue;
    const cs = getComputedStyle(node);
    const hasDirectText = Array.from(node.childNodes).some(
      (n) => n.nodeType === 3 && n.textContent.trim().length > 0
    );
    if (hasDirectText) {
      checkedTextNodes += 1;
      const fg = parseRgba(cs.color);
      const bg = resolveBg(node);
      if (fg && bg) {
        const fgComp = fg.a < 1 ? composite(fg, bg) : fg;
        const cr = ratio(fgComp, bg);
        const fs = parseFloat(cs.fontSize) || 14;
        const fw = parseInt(cs.fontWeight, 10) || 400;
        const isLarge = fs >= 24 || (fs >= 18.66 && fw >= 700);
        const minCr = isLarge ? 3.0 : 4.5;
        if (cr < minCr) {
          contrastFailures.push({
            tag: node.tagName.toLowerCase(),
            className: typeof node.className === 'string' ? node.className.slice(0, 48) : '',
            text: node.textContent.trim().slice(0, 48),
            ratio: Number(cr.toFixed(2)),
            required: minCr,
          });
        }
      }
      const ox = cs.overflowX;
      const oy = cs.overflowY;
      if (
        (ox === 'hidden' || ox === 'clip') &&
        node.clientWidth > 0 &&
        node.scrollWidth > node.clientWidth + 4
      ) {
        clippedElements.push({
          axis: 'x',
          tag: node.tagName.toLowerCase(),
          text: node.textContent.trim().slice(0, 48),
          scroll: node.scrollWidth,
          client: node.clientWidth,
        });
      }
      if (
        (oy === 'hidden' || oy === 'clip') &&
        node.clientHeight > 0 &&
        node.scrollHeight > node.clientHeight + 4
      ) {
        clippedElements.push({
          axis: 'y',
          tag: node.tagName.toLowerCase(),
          text: node.textContent.trim().slice(0, 48),
          scroll: node.scrollHeight,
          client: node.clientHeight,
        });
      }
    }
  }

  const isFixedDesktopApp = (() => {
    if (document.body && document.body.getAttribute('data-platform') === 'desktop') return true;
    const app = document.querySelector('.app');
    if (!app) return false;
    const cs = getComputedStyle(app);
    return parseFloat(cs.width) >= 1200 && cs.overflow === 'hidden';
  })();

  return {
    innerWidth: window.innerWidth,
    scrollWidth: docEl.scrollWidth,
    overflowX,
    isFixedDesktopApp,
    checkedTextNodes,
    contrastFailures: contrastFailures.slice(0, 12),
    clippedElements: clippedElements.slice(0, 12),
  };
})()"""


def run_ab(session: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["agent-browser", "--session", session, *args],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def audit_file(
    path: str, screenshot_dir: str | None = None, viewport_mode: str = "auto"
) -> dict:
    abs_path = os.path.abspath(path)
    url = f"file://{abs_path}"
    session = f"va-{uuid.uuid4().hex[:8]}"
    viewports_out = []
    blockers = []

    if viewport_mode == "desktop":
        targets = [VIEWPORTS[0]]
    elif viewport_mode == "mobile":
        targets = [VIEWPORTS[1]]
    else:
        targets = list(VIEWPORTS)

    try:
        open_res = run_ab(session, "open", url)
        if open_res.returncode != 0:
            return {
                "file": os.path.normpath(path),
                "error": open_res.stderr.strip() or open_res.stdout.strip(),
                "blockers": ["failed to open artboard in agent-browser"],
                "viewports": [],
            }

        for vp_name, width, height in targets:
            run_ab(session, "set", "viewport", str(width), str(height))
            run_ab(session, "wait", "150")
            eval_res = run_ab(session, "eval", AUDIT_JS)
            if eval_res.returncode != 0:
                blockers.append(
                    f"{vp_name} ({width}x{height}): eval error: {eval_res.stderr.strip()}"
                )
                continue

            raw_out = eval_res.stdout.strip()
            try:
                metrics = json.loads(raw_out)
                if isinstance(metrics, str):
                    metrics = json.loads(metrics)
            except json.JSONDecodeError:
                blockers.append(
                    f"{vp_name} ({width}x{height}): unparseable eval output: {raw_out[:160]}"
                )
                continue

            if viewport_mode == "auto" and vp_name == "mobile" and metrics.get("isFixedDesktopApp"):
                continue

            if screenshot_dir:
                os.makedirs(screenshot_dir, exist_ok=True)
                stem = os.path.splitext(os.path.basename(path))[0]
                shot_path = os.path.join(screenshot_dir, f"{stem}-{vp_name}.png")
                run_ab(session, "screenshot", shot_path)
                metrics["screenshot"] = shot_path

            viewports_out.append({"name": vp_name, "width": width, "height": height, **metrics})

            if metrics.get("overflowX", 0) > 2:
                blockers.append(
                    f"{vp_name} ({width}px): horizontal overflow +{metrics['overflowX']}px "
                    f"(scrollWidth={metrics['scrollWidth']})"
                )
            for cf in metrics.get("contrastFailures", []):
                blockers.append(
                    f"{vp_name}: contrast {cf['ratio']}:1 (< {cf['required']}:1) "
                    f"on <{cf['tag']}> \"{cf['text']}\""
                )
            for cl in metrics.get("clippedElements", []):
                blockers.append(
                    f"{vp_name}: clipped-{cl['axis']} ({cl['scroll']} > {cl['client']}) "
                    f"on <{cl['tag']}> \"{cl['text']}\""
                )
    finally:
        run_ab(session, "close")

    return {
        "file": os.path.normpath(path),
        "viewports": viewports_out,
        "blockers": blockers,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="visual-audit.py",
        description="Dynamic browser visual audit (overflow, contrast, clipping) via agent-browser.",
    )
    parser.add_argument("files", nargs="*", metavar="artboard.html")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument("--screenshot-dir", help="Optional directory to store viewport PNGs")
    parser.add_argument(
        "--viewport",
        choices=("auto", "both", "desktop", "mobile"),
        default="auto",
        help="Viewports to audit (default: auto)",
    )
    args = parser.parse_args(argv)

    if not args.files:
        parser.error("no artboard files given")

    if not shutil.which("agent-browser"):
        print("visual-audit: agent-browser not found in PATH", file=sys.stderr)
        return 2

    results = []
    for path in args.files:
        if not os.path.isfile(path):
            print(f"visual-audit: file not found: {path}", file=sys.stderr)
            return 2
        results.append(audit_file(path, args.screenshot_dir, args.viewport))

    if args.json:
        doc = results[0] if len(results) == 1 else results
        print(json.dumps(doc, indent=2, ensure_ascii=False))
    else:
        for res in results:
            if res["blockers"]:
                for b in res["blockers"]:
                    print(f"{res['file']}: [BLOCKER] {b}")
            else:
                vps = ", ".join(
                    f"{v['name']}:{v['checkedTextNodes']}txt/0ovf" for v in res["viewports"]
                )
                print(f"{res['file']}: [VERDE] {vps}")

    return 1 if any(r["blockers"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
