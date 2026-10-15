#!/usr/bin/env python3
"""
SessionStart hook: refreshes the project's Graphify graph when a session starts and after each
compaction, so `graphify query` and the strict Read hook work on current code.

It runs `graphify update .` (code only, local, no LLM) in the background and prints nothing, so it
adds no tokens and does not delay the session. It does nothing when the project has no
graphify-out/graph.json or the graphify CLI is not installed. GOD_MODE_GRAPHIFY_REFRESH=off turns
it off.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SOURCES = {"startup", "compact"}


def graphify_bin():
    found = shutil.which("graphify")
    if found:
        return found
    # The desktop app may start Claude Code without ~/.local/bin on PATH, where `uv tool` installs it.
    fallback = Path.home() / ".local" / "bin" / "graphify"
    return str(fallback) if fallback.is_file() and os.access(fallback, os.X_OK) else None


def main():
    if os.environ.get("GOD_MODE_GRAPHIFY_REFRESH", "").strip().lower() == "off":
        return 0
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if data.get("source") not in SOURCES:
        return 0
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    if not (project / "graphify-out" / "graph.json").is_file():
        return 0
    binary = graphify_bin()
    if not binary:
        return 0
    env = dict(os.environ, PYTHONHASHSEED="0", GRAPHIFY_NO_TIPS="1")
    subprocess.Popen([binary, "update", "."], cwd=project, env=env, stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
