#!/usr/bin/env python3
"""sync-check.py — anti-drift verification for installed copies of a skill tree.

`gentle-design-skill` is installed to several roots that must stay identical
(`~/.agents/skills/`, the working repo, the public repo). This script compares trees
by relative path and SHA-256 of the raw bytes, so drift is detected exactly and
without diff noise. Python 3 standard library only, no network.

Usage
-----
    python3 sync-check.py manifest SRC
    python3 sync-check.py verify SRC MANIFEST.json
    python3 sync-check.py compare SRC DEST [DEST ...]

    manifest  print {"root": <abs>, "files": {"<relpath>": "<sha256>"}} as JSON
    verify    exit 0 only when SRC matches the manifest exactly
    compare   human-readable drift table between SRC and each DEST

Exit codes
----------
    0  in sync (verify: exact match; compare: every DEST matches SRC)
    1  drift (verify: missing/extra/changed files; compare: any DEST differs)
    2  usage error (missing argument, nonexistent path, unreadable/invalid manifest)

What is compared
----------------
Regular files only, keyed by POSIX relative path. Empty directories carry no content
and are ignored. Also ignored at any depth, because they are regenerated or out of
scope:

    __pycache__/       byte-cache, rebuilt by every interpreter
    *.pyc              compiled bytecode
    hidden files/dirs  any path component starting with "." (".git", ".DS_Store")
    *.json             design manifests ("design.json") and the sync manifest itself

Manifest schema
---------------
    {"root": "<absolute path>", "files": {"<relpath>": "<sha256>"}}

`root` records where the manifest was produced. `verify` treats it as informational,
so one manifest can validate a copy that lives at a different absolute path; the
`files` map is the contract. Keep the manifest outside the compared tree, or inside
it as `sync-manifest.json` — JSON files are ignored either way.

Examples
--------
    python3 sync-check.py manifest ~/.agents/skills/gentle-design-skill > sync-manifest.json
    python3 sync-check.py verify ~/.agents/skills/gentle-design-skill sync-manifest.json
    python3 sync-check.py compare skill/gentle-design-skill ~/.agents/skills/gentle-design-skill
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

IGNORED_DIR_NAMES = frozenset({"__pycache__"})
IGNORED_SUFFIXES = (".pyc", ".json")
CHUNK_SIZE = 1 << 20


def is_ignored_component(name: str) -> bool:
    """True when a path component takes its whole subtree out of scope."""
    return name.startswith(".") or name in IGNORED_DIR_NAMES


def is_ignored_file(name: str) -> bool:
    """True when a file name takes the file out of scope."""
    return is_ignored_component(name) or name.endswith(IGNORED_SUFFIXES)


def hash_file(path: str) -> str:
    """SHA-256 of the raw bytes, chunked so large files stay memory-cheap."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_tree(root: str) -> dict[str, str]:
    """Map POSIX relative path -> sha256 for every comparable file, sorted."""
    root = os.path.abspath(root)
    hashes: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if not is_ignored_component(name))
        for name in sorted(filenames):
            if is_ignored_file(name):
                continue
            full = os.path.join(dirpath, name)
            if not os.path.isfile(full):
                continue
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            hashes[rel] = hash_file(full)
    return dict(sorted(hashes.items()))


def diff_trees(src: dict[str, str], dest: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    """Return (only in src, only in dest, changed) as sorted relative paths."""
    src_keys, dest_keys = set(src), set(dest)
    only_src = sorted(src_keys - dest_keys)
    only_dest = sorted(dest_keys - src_keys)
    changed = sorted(path for path in src_keys & dest_keys if src[path] != dest[path])
    return only_src, only_dest, changed


def load_manifest(path: str) -> dict[str, str]:
    """Read and validate the `files` map; raise ValueError on a schema mismatch."""
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), dict):
        raise ValueError('expected {"root": string, "files": {relpath: sha256}}')
    files = payload["files"]
    for rel, digest in files.items():
        if not isinstance(rel, str) or not isinstance(digest, str):
            raise ValueError("'files' entries must map a path string to a sha256 string")
    return files


def path_problem(path: str, kind: str) -> str | None:
    """Return a usage-error message for a bad path, else None."""
    if not os.path.exists(path):
        return f"no such {kind}: {path}"
    if kind == "directory" and not os.path.isdir(path):
        return f"not a directory: {path}"
    if kind == "file" and not os.path.isfile(path):
        return f"not a file: {path}"
    return None


def fail(message: str) -> int:
    print(f"sync-check: {message}", file=sys.stderr)
    return 2


def cmd_manifest(src: str) -> int:
    payload = {"root": os.path.abspath(src), "files": scan_tree(src)}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def cmd_verify(src: str, manifest_path: str) -> int:
    manifest = os.path.abspath(manifest_path)
    try:
        expected = load_manifest(manifest)
    except (OSError, ValueError) as exc:
        return fail(f"cannot read manifest {manifest_path}: {exc}")

    missing, extra, changed = diff_trees(expected, scan_tree(src))
    for rel in missing:
        print(f"missing: {rel}", file=sys.stderr)
    for rel in extra:
        print(f"extra: {rel}", file=sys.stderr)
    for rel in changed:
        print(f"changed: {rel}", file=sys.stderr)

    if missing or extra or changed:
        print(
            f"verify: {len(missing) + len(extra) + len(changed)} problem(s) vs {manifest} "
            f"({len(missing)} missing, {len(extra)} extra, {len(changed)} changed)"
        )
        return 1
    print(f"verify: OK ({len(expected)} file(s) match {manifest})")
    return 0


def cmd_compare(src: str, dests: list[str]) -> int:
    src_abs = os.path.abspath(src)
    src_files = scan_tree(src_abs)
    differing = 0
    for dest in dests:
        dest_abs = os.path.abspath(dest)
        only_src, only_dest, changed = diff_trees(src_files, scan_tree(dest_abs))
        print(f"== {src_abs} vs {dest_abs} ==")
        if not (only_src or only_dest or changed):
            print(f"  in sync ({len(src_files)} file(s))")
            continue
        differing += 1
        for rel in only_src:
            print(f"  only-in-src   {rel}")
        for rel in only_dest:
            print(f"  only-in-dest  {rel}")
        for rel in changed:
            print(f"  changed       {rel}")
        print(
            f"  drift: {len(only_src) + len(only_dest) + len(changed)} file(s) differ "
            f"(only-in-src={len(only_src)} only-in-dest={len(only_dest)} changed={len(changed)})"
        )
    print(f"compare: {differing} of {len(dests)} root(s) differ")
    return 1 if differing else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sync-check.py",
        description=(
            "Anti-drift verification for installed copies of a skill tree: compare by "
            "relative path + SHA-256 of the raw bytes."
        ),
        epilog=(
            "Subcommands:\n"
            '  manifest SRC                print {"root": ..., "files": {relpath: sha256}} JSON\n'
            "  verify SRC MANIFEST.json    exit 0 only when SRC matches the manifest exactly\n"
            "  compare SRC DEST [DEST...]  drift table (only-in-src / only-in-dest / changed) "
            "per DEST\n"
            "\n"
            "Ignored in every tree: __pycache__/, *.pyc, hidden files and directories, and\n"
            "*.json design manifests (design.json, sync-manifest.json).\n"
            "\n"
            "Exit codes: 0 in sync, 1 drift, 2 usage error."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subcommands = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)

    manifest = subcommands.add_parser(
        "manifest",
        help="print the SHA-256 manifest of SRC as JSON",
        description="Print the SHA-256 manifest of SRC as JSON, sorted by relative path.",
    )
    manifest.add_argument("src", metavar="SRC", help="tree to fingerprint")

    verify = subcommands.add_parser(
        "verify",
        help="verify SRC against a manifest (exit 1 on any drift)",
        description=(
            "Exit 0 only when every file in SRC matches the manifest exactly: no missing, "
            "no extra, no changed files."
        ),
    )
    verify.add_argument("src", metavar="SRC", help="tree to verify")
    verify.add_argument("manifest", metavar="MANIFEST.json", help="manifest produced by 'manifest'")

    compare = subcommands.add_parser(
        "compare",
        help="table of drift between SRC and each DEST",
        description=(
            "Print a human-readable table of drift between SRC and each DEST "
            "(files only in SRC, only in DEST, changed)."
        ),
    )
    compare.add_argument("src", metavar="SRC", help="reference tree")
    compare.add_argument("dests", nargs="+", metavar="DEST", help="tree(s) to compare against SRC")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one subcommand and return the process exit code (never raises SystemExit)."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse already printed help or usage to the right stream
        return 0 if exc.code in (0, None) else 2

    if args.command == "manifest":
        problem = path_problem(args.src, "directory")
        return fail(problem) if problem else cmd_manifest(args.src)

    if args.command == "verify":
        problem = path_problem(args.src, "directory")
        if problem:
            return fail(problem)
        problem = path_problem(args.manifest, "file")
        return fail(problem) if problem else cmd_verify(args.src, args.manifest)

    for path in (args.src, *args.dests):
        problem = path_problem(path, "directory")
        if problem:
            return fail(problem)
    return cmd_compare(args.src, args.dests)


if __name__ == "__main__":
    sys.exit(main())
