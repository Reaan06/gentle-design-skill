#!/usr/bin/env python3
"""Unit tests for skill/gentle-design-skill/scripts/visual-audit.py."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_CANDIDATES = (
    os.path.join(REPO_ROOT, "skill", "gentle-design-skill", "scripts", "visual-audit.py"),
    os.path.join(REPO_ROOT, "skill", "scripts", "visual-audit.py"),
)
AUDIT_PATH = next((p for p in AUDIT_CANDIDATES if os.path.isfile(p)), AUDIT_CANDIDATES[0])

spec = importlib.util.spec_from_file_location("visual_audit", AUDIT_PATH)
visual_audit = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(visual_audit)


def _ok(stdout: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["agent-browser"], 0, stdout=stdout, stderr="")


def _fail(stderr: str = "boom") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(["agent-browser"], 1, stdout="", stderr=stderr)


def _metrics(
    *,
    inner_width: int = 1440,
    overflow_x: int = 0,
    fixed_desktop: bool = False,
    checked_text: int = 42,
    contrast_failures: list | None = None,
    clipped: list | None = None,
) -> str:
    return json.dumps(
        {
            "innerWidth": inner_width,
            "scrollWidth": inner_width + overflow_x,
            "overflowX": overflow_x,
            "isFixedDesktopApp": fixed_desktop,
            "checkedTextNodes": checked_text,
            "contrastFailures": contrast_failures or [],
            "clippedElements": clipped or [],
        }
    )


class VisualAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.html_path = os.path.join(self._tmp.name, "sample.html")
        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write("<!doctype html><html><body><p>Hello</p></body></html>")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_missing_agent_browser_returns_2(self) -> None:
        err = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value=None):
            with redirect_stderr(err):
                rc = visual_audit.main([self.html_path])
        self.assertEqual(rc, 2)
        self.assertIn("agent-browser not found", err.getvalue())

    def test_missing_file_returns_2(self) -> None:
        err = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value="/usr/bin/agent-browser"):
            with redirect_stderr(err):
                rc = visual_audit.main([os.path.join(self._tmp.name, "missing.html")])
        self.assertEqual(rc, 2)
        self.assertIn("file not found", err.getvalue())

    def test_clean_both_viewports_returns_0_and_verde(self) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_run(session: str, *args: str):
            calls.append(args)
            if args[0] == "eval":
                if ("set", "viewport", "390", "844") in calls:
                    return _ok(_metrics(inner_width=390, checked_text=30))
                return _ok(_metrics(inner_width=1440, checked_text=40))
            return _ok()

        out = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value="/usr/bin/agent-browser"):
            with mock.patch.object(visual_audit, "run_ab", side_effect=fake_run):
                with redirect_stdout(out):
                    rc = visual_audit.main([self.html_path])

        self.assertEqual(rc, 0)
        self.assertIn("[VERDE] desktop:40txt/0ovf, mobile:30txt/0ovf", out.getvalue())
        self.assertEqual(calls[-1], ("close",))

    def test_auto_skips_mobile_for_fixed_desktop_app_but_both_includes_it(self) -> None:
        state = {"vp": "desktop"}

        def fake_run_vp(session: str, *args: str):
            if args[:2] == ("set", "viewport"):
                state["vp"] = "desktop" if args[2] == "1440" else "mobile"
                return _ok()
            if args[0] == "eval":
                if state["vp"] == "desktop":
                    return _ok(_metrics(inner_width=1440, overflow_x=0, fixed_desktop=True, checked_text=90))
                return _ok(_metrics(inner_width=390, overflow_x=1050, fixed_desktop=True, checked_text=90))
            return _ok()

        out_auto = io.StringIO()
        out_both = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value="/usr/bin/agent-browser"):
            with mock.patch.object(visual_audit, "run_ab", side_effect=fake_run_vp):
                with redirect_stdout(out_auto):
                    rc_auto = visual_audit.main([self.html_path, "--viewport", "auto"])
                with redirect_stdout(out_both):
                    rc_both = visual_audit.main([self.html_path, "--viewport", "both"])

        self.assertEqual(rc_auto, 0)
        self.assertIn("[VERDE] desktop:90txt/0ovf", out_auto.getvalue())
        self.assertNotIn("mobile:", out_auto.getvalue())

        self.assertEqual(rc_both, 1)
        self.assertIn("[BLOCKER] mobile (390px): horizontal overflow +1050px", out_both.getvalue())

    def test_detects_overflow_contrast_and_clipping_in_json(self) -> None:
        state = {"vp": "desktop"}

        def fake_run(session: str, *args: str):
            if args[:2] == ("set", "viewport"):
                state["vp"] = "desktop" if args[2] == "1440" else "mobile"
                return _ok()
            if args[0] == "eval":
                if state["vp"] == "desktop":
                    return _ok(
                        _metrics(
                            inner_width=1440,
                            contrast_failures=[
                                {"tag": "span", "className": "muted", "text": "Low contrast", "ratio": 2.9, "required": 4.5}
                            ],
                        )
                    )
                return _ok(
                    _metrics(
                        inner_width=390,
                        overflow_x=48,
                        clipped=[{"axis": "x", "tag": "div", "text": "Cut off", "scroll": 220, "client": 180}],
                    )
                )
            return _ok()

        out = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value="/usr/bin/agent-browser"):
            with mock.patch.object(visual_audit, "run_ab", side_effect=fake_run):
                with redirect_stdout(out):
                    rc = visual_audit.main([self.html_path, "--json"])

        self.assertEqual(rc, 1)
        payload = json.loads(out.getvalue())
        self.assertEqual(len(payload["blockers"]), 3)
        joined = "\n".join(payload["blockers"])
        self.assertIn("contrast 2.9:1 (< 4.5:1)", joined)
        self.assertIn("horizontal overflow +48px", joined)
        self.assertIn("clipped-x (220 > 180)", joined)

    def test_screenshot_dir_and_viewport_desktop_only(self) -> None:
        shots_dir = os.path.join(self._tmp.name, "shots")
        seen_cmds: list[tuple[str, ...]] = []

        def fake_run(session: str, *args: str):
            seen_cmds.append(args)
            if args[0] == "eval":
                return _ok(_metrics(inner_width=1440, checked_text=12))
            return _ok()

        out = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value="/usr/bin/agent-browser"):
            with mock.patch.object(visual_audit, "run_ab", side_effect=fake_run):
                with redirect_stdout(out):
                    rc = visual_audit.main(
                        [self.html_path, "--viewport", "desktop", "--screenshot-dir", shots_dir, "--json"]
                    )

        self.assertEqual(rc, 0)
        payload = json.loads(out.getvalue())
        self.assertEqual(len(payload["viewports"]), 1)
        expected_shot = os.path.join(shots_dir, "sample-desktop.png")
        self.assertEqual(payload["viewports"][0]["screenshot"], expected_shot)
        self.assertIn(("screenshot", expected_shot), seen_cmds)
        self.assertTrue(os.path.isdir(shots_dir))

    def test_open_failure_returns_blocker_and_closes_session(self) -> None:
        seen_cmds: list[tuple[str, ...]] = []

        def fake_run(session: str, *args: str):
            seen_cmds.append(args)
            if args[0] == "open":
                return _fail("cannot open file")
            return _ok()

        out = io.StringIO()
        with mock.patch.object(visual_audit.shutil, "which", return_value="/usr/bin/agent-browser"):
            with mock.patch.object(visual_audit, "run_ab", side_effect=fake_run):
                with redirect_stdout(out):
                    rc = visual_audit.main([self.html_path])

        self.assertEqual(rc, 1)
        self.assertIn("failed to open artboard in agent-browser", out.getvalue())
        self.assertEqual(seen_cmds[-1], ("close",))


if __name__ == "__main__":
    unittest.main()
