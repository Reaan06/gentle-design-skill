#!/usr/bin/env python3
"""Unit tests for skill/gentle-design-skill/scripts/design-gate.py (R1-R17)."""

from __future__ import annotations

import glob
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE_CANDIDATES = (
    os.path.join(REPO_ROOT, "skill", "gentle-design-skill", "scripts", "design-gate.py"),
    os.path.join(REPO_ROOT, "skill", "scripts", "design-gate.py"),
)
GATE_PATH = next((p for p in GATE_CANDIDATES if os.path.isfile(p)), GATE_CANDIDATES[0])

spec = importlib.util.spec_from_file_location("design_gate", GATE_PATH)
design_gate = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(design_gate)


VALID_ROOT_CSS = """
:root {
  --background: #ffffff;
  --foreground: #0b1210;
  --card: #ffffff;
  --card-foreground: #0b1210;
  --primary: #0b5f4f;
  --primary-foreground: #ffffff;
  --secondary: #f3f4f6;
  --muted: #f3f4f6;
  --muted-foreground: #596663;
  --accent: #f3f4f6;
  --destructive: #dc2626;
  --border: #e5e7eb;
  --input: #d1d5db;
  --ring: #0b5f4f;
  --radius: 0.625rem;
}
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--background);
  color: var(--foreground);
}
.btn {
  border-radius: var(--radius);
  background: var(--primary);
  color: var(--primary-foreground);
  padding: 8px 16px;
  transition: background-color 180ms ease-out;
}
:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
"""


def make_html(css: str = VALID_ROOT_CSS, body: str = '<button class="btn">Save</button>') -> str:
    return f"<!doctype html><html><head><style>{css}</style></head><body>{body}</body></html>"


def rule_ids(findings: list[dict]) -> list[str]:
    return [f["rule"].split()[0] for f in findings]


class DesignGateTests(unittest.TestCase):
    def test_valid_baseline_is_clean(self):
        findings = design_gate.Gate("ok.html", make_html()).run()
        self.assertEqual(findings, [])

    def test_r1_missing_root_and_tokens(self):
        findings = design_gate.Gate("no-root.html", make_html(css="body { margin: 8px; }")).run()
        self.assertIn("R1", rule_ids(findings))

    def test_r2_raw_color_outside_root(self):
        css = VALID_ROOT_CSS + ".chip { color: #ff0000; }"
        findings = design_gate.Gate("raw-color.html", make_html(css=css)).run()
        self.assertIn("R2", rule_ids(findings))

    def test_r3_off_ramp_spacing(self):
        css = VALID_ROOT_CSS + ".box { padding: 14px; }"
        findings = design_gate.Gate("spacing.html", make_html(css=css)).run()
        self.assertIn("R3", rule_ids(findings))

    def test_r4_transition_all(self):
        css = VALID_ROOT_CSS + ".box { transition: all 150ms ease; }"
        findings = design_gate.Gate("trans.html", make_html(css=css)).run()
        self.assertIn("R4", rule_ids(findings))

    def test_r5_missing_reduced_motion(self):
        css = VALID_ROOT_CSS + "@keyframes rise { from { opacity: 0; } to { opacity: 1; } }"
        findings = design_gate.Gate("motion.html", make_html(css=css)).run()
        self.assertIn("R5", rule_ids(findings))

    def test_r6_missing_focus_visible(self):
        css = VALID_ROOT_CSS.replace(":focus-visible", ".noop")
        findings = design_gate.Gate("focus.html", make_html(css=css)).run()
        self.assertIn("R6", rule_ids(findings))

    def test_r7_inter_first_tell(self):
        css = VALID_ROOT_CSS.replace("system-ui", "Inter")
        findings = design_gate.Gate("font.html", make_html(css=css)).run()
        self.assertIn("R7", rule_ids(findings))

    def test_r8_slop_gradient(self):
        css = VALID_ROOT_CSS + ".hero { background: linear-gradient(135deg, #6366f1, #8b5cf6); }"
        findings = design_gate.Gate("slop.html", make_html(css=css)).run()
        self.assertIn("R8", rule_ids(findings))

    def test_r9_emoji_icon_in_button(self):
        findings = design_gate.Gate("emoji.html", make_html(body='<button class="btn">🚀 Launch</button>')).run()
        self.assertIn("R9", rule_ids(findings))

    def test_r10_numbered_marker_heading(self):
        findings = design_gate.Gate("num.html", make_html(body='<button class="btn">Save</button><h3>01 — Fast</h3>')).run()
        self.assertIn("R10", rule_ids(findings))

    def test_r11_radius_drift(self):
        css = VALID_ROOT_CSS + ".pill { border-radius: 13px; }"
        findings = design_gate.Gate("rad.html", make_html(css=css)).run()
        self.assertIn("R11", rule_ids(findings))

    def test_r12_transition_duration_tell(self):
        css = VALID_ROOT_CSS + ".slow { transition: opacity 900ms ease-out; }"
        findings = design_gate.Gate("dur.html", make_html(css=css)).run()
        self.assertIn("R12", rule_ids(findings))

    # --- v1.1.0 rules (R13-R17) ---

    def test_r13_missing_primary_foreground_token(self):
        css = VALID_ROOT_CSS.replace("--primary-foreground: #ffffff;", "").replace(
            "color: var(--primary-foreground);", "color: var(--background);"
        )
        findings = design_gate.Gate("no-on-primary.html", make_html(css=css)).run()
        self.assertIn("R13", rule_ids(findings))

    def test_r13_primary_bg_paired_with_foreground_text(self):
        css = VALID_ROOT_CSS + ".bad-cta { background: var(--primary); color: var(--foreground); }"
        findings = design_gate.Gate("bad-pair.html", make_html(css=css)).run()
        self.assertIn("R13", rule_ids(findings))

    def test_r14_border_on_layout_wrapper(self):
        css = VALID_ROOT_CSS + ".section { border: 1px solid var(--border); padding: 24px; }"
        findings = design_gate.Gate("wrapper-border.html", make_html(css=css)).run()
        self.assertIn("R14", rule_ids(findings))

    def test_r14_allows_single_edge_divider_or_interactive_border(self):
        css = VALID_ROOT_CSS + ".section { border-top: 1px solid var(--border); } .card { border: 1px solid var(--border); }"
        findings = design_gate.Gate("divider-ok.html", make_html(css=css)).run()
        self.assertNotIn("R14", rule_ids(findings))

    def test_r15_micro_text_below_12px(self):
        css = VALID_ROOT_CSS + ".caption { font-size: 10px; }"
        findings = design_gate.Gate("micro.html", make_html(css=css)).run()
        self.assertIn("R15", rule_ids(findings))

    def test_r15_micro_text_rem_below_075(self):
        css = VALID_ROOT_CSS + ".caption { font-size: 0.625rem; }"
        findings = design_gate.Gate("micro-rem.html", make_html(css=css)).run()
        self.assertIn("R15", rule_ids(findings))

    def test_r16_svg_missing_dimensions(self):
        body = '<button class="btn"><svg viewBox="0 0 16 16"></svg>Save</button>'
        findings = design_gate.Gate("svg.html", make_html(body=body)).run()
        self.assertIn("R16", rule_ids(findings))

    def test_r16_img_missing_alt_or_dimensions(self):
        body = '<button class="btn">Save</button><img src="a.png">'
        findings = design_gate.Gate("img.html", make_html(body=body)).run()
        self.assertIn("R16", rule_ids(findings))

    def test_r17_low_contrast_root_pair(self):
        css = VALID_ROOT_CSS.replace("--muted-foreground: #596663;", "--muted-foreground: #cbd5e1;")
        findings = design_gate.Gate("contrast.html", make_html(css=css)).run()
        self.assertIn("R17", rule_ids(findings))

    def test_cli_json_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok_path = os.path.join(tmp, "ok.html")
            bad_path = os.path.join(tmp, "bad.html")
            with open(ok_path, "w", encoding="utf-8") as f:
                f.write(make_html())
            with open(bad_path, "w", encoding="utf-8") as f:
                f.write(make_html(css=VALID_ROOT_CSS + ".x { padding: 13px; }"))

            res_ok = subprocess.run(
                [sys.executable, GATE_PATH, ok_path, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res_ok.returncode, 0)
            self.assertEqual(json.loads(res_ok.stdout)["findings"], [])

            res_bad = subprocess.run(
                [sys.executable, GATE_PATH, bad_path, "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res_bad.returncode, 1)
            self.assertEqual(rule_ids(json.loads(res_bad.stdout)["findings"]), ["R3"])

    def test_repo_artboards_pass_gate(self):
        artboards = sorted(glob.glob(os.path.join(REPO_ROOT, "design", "*", "*.html")))
        if not artboards:
            artboards = sorted(glob.glob(os.path.join(REPO_ROOT, "examples", "*", "*.html")))
        self.assertGreater(len(artboards), 0, "Expected sample artboards to verify")
        for path in artboards:
            with open(path, "r", encoding="utf-8") as f:
                findings = design_gate.Gate(path, f.read()).run()
            self.assertEqual(findings, [], f"{path} produced unexpected findings: {findings}")


if __name__ == "__main__":
    unittest.main()
