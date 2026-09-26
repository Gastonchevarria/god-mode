#!/usr/bin/env python3
"""
Runs the vendored archify skill's own test suite.

archify's `npm test` expects the upstream archify repository layout (../scripts, ../docs, ...),
so it cannot run from plugins/god-mode-core/skills/archify. This runner checks the generated
files, then runs every test except the upstream-repository ones listed in config/archify-tests.json,
and fails if that list goes stale.

Usage: npm ci --prefix plugins/god-mode-core/skills/archify && python3 scripts/test_archify.py
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIFY = ROOT / "plugins" / "god-mode-core" / "skills" / "archify"
CONFIG = ROOT / "config" / "archify-tests.json"
GENERATED_CHECKS = (
    ["node", "scripts/generate-brand-marks.mjs", "--check"],
    ["node", "scripts/generate-validators.mjs", "--check"],
)


def js_regex_literal(text):
    """Anchored pattern for node --test-skip-pattern that matches exactly this test name."""
    return "^" + re.sub(r"([.*+?^${}()|\[\]\\/])", r"\\\1", text) + "$"


def stale_entries(config):
    problems = []
    for entry in config["excluded_files"]:
        if not (ARCHIFY / entry["file"]).is_file():
            problems.append(f"excluded file no longer exists: {entry['file']}")
    for entry in config["excluded_tests"]:
        path = ARCHIFY / entry["file"]
        if not path.is_file():
            problems.append(f"file of excluded test no longer exists: {entry['file']}")
        elif entry["name"] not in path.read_text(encoding="utf-8"):
            problems.append(f"excluded test not found in {entry['file']}: {entry['name']}")
    return problems


def main():
    if shutil.which("node") is None:
        sys.exit("node is required to run the archify tests.")
    if not (ARCHIFY / "node_modules").is_dir():
        sys.exit(f"Install archify's dev dependencies first: npm ci --prefix {ARCHIFY.relative_to(ROOT)}")

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    problems = stale_entries(config)
    if problems:
        print("config/archify-tests.json is out of date:", *problems, sep="\n  ", file=sys.stderr)
        sys.exit(1)

    for check in GENERATED_CHECKS:
        print(f"$ {' '.join(check)}", flush=True)
        if subprocess.run(check, cwd=ARCHIFY, check=False).returncode != 0:
            sys.exit(1)

    excluded = {entry["file"] for entry in config["excluded_files"]}
    files = sorted(str(p.relative_to(ARCHIFY)) for p in (ARCHIFY / "test").glob("*.test.mjs"))
    files = [f for f in files if f not in excluded]
    skips = [arg for entry in config["excluded_tests"]
             for arg in ("--test-skip-pattern", js_regex_literal(entry["name"]))]

    print(f"$ node --test ({len(files)} files, {len(excluded)} files and "
          f"{len(config['excluded_tests'])} tests excluded as upstream-only)", flush=True)
    result = subprocess.run(["node", "--test", *skips, *files], cwd=ARCHIFY, check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
