#!/usr/bin/env python3
"""
Routing evaluation: does Claude pick the right god-mode skill for a request?

Loads the plugins with `claude -p --plugin-dir ...` in an isolated HOME (so no other
installed plugins interfere), sends each request, and records the first Skill tool
call. A case passes when that skill is one of the expected ones.

Usage:
    python3 scripts/eval_routing.py [--plugins-root plugins] [--cases tests/evals/routing.json]
                                    [--workers 6] [--runs 1] [--model MODEL] [--out report.json]

Requires the Claude Code CLI (`claude`) with working authentication.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERROR = "ERROR"
# Variables that tie a child `claude` process to the session that launched it. They are
# removed so every eval run is an independent session; authentication variables are kept.
KEEP_CLAUDE_VARS = {"CLAUDE_SESSION_INGRESS_TOKEN_FILE", "CLAUDE_CODE_OAUTH_TOKEN"}


def isolated_env(home):
    env = {k: v for k, v in os.environ.items()
           if not (k.startswith("CLAUDE") and k not in KEEP_CLAUDE_VARS)}
    env.update(HOME=str(home), CLAUDE_CODE_SYNC_PLUGINS="0", CLAUDE_CODE_SYNC_SKILLS="0")
    return env


def first_skill_call(query, plugin_dirs, home, model, timeout, retries=1):
    """First skill invoked (without plugin prefix), None if no skill was used, ERROR if the run failed."""
    for _ in range(retries + 1):
        picked = _run_once(query, plugin_dirs, home, model, timeout)
        if picked != ERROR:
            return picked
    return ERROR


def _run_once(query, plugin_dirs, home, model, timeout):
    cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose",
           "--include-partial-messages", "--max-turns", "2"]
    for d in plugin_dirs:
        cmd += ["--plugin-dir", str(d)]
    if model:
        cmd += ["--model", model]
    workdir = tempfile.mkdtemp(dir=home)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                            env=isolated_env(home), cwd=workdir)
    deadline = time.time() + timeout
    partial = {}
    try:
        for line in proc.stdout:
            if time.time() > deadline:
                break
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            found = _skill_from_event(event, partial)
            if found is not None:
                return found
            if event.get("type") == "result":
                return ERROR if event.get("is_error") else None
            if event.get("type") == "assistant" and _answered_in_text(event):
                return None
    finally:
        proc.kill()
        proc.wait()
    return ERROR


def _answered_in_text(event):
    blocks = event.get("message", {}).get("content", [])
    return any(b.get("type") == "text" and b.get("text", "").strip() for b in blocks) and \
        not any(b.get("type") == "tool_use" for b in blocks)


def _skill_from_event(event, partial):
    if event.get("type") == "assistant":
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                return _strip(block.get("input", {}).get("skill", ""))
    if event.get("type") == "stream_event":
        ev = event.get("event", {})
        if ev.get("type") == "content_block_start":
            block = ev.get("content_block", {})
            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                partial[ev.get("index")] = ""
        elif ev.get("type") == "content_block_delta" and ev.get("index") in partial:
            partial[ev["index"]] += ev.get("delta", {}).get("partial_json", "")
            try:
                return _strip(json.loads(partial[ev["index"]]).get("skill", ""))
            except json.JSONDecodeError:
                return None
    return None


def _strip(name):
    return name.split(":", 1)[-1].lstrip("/") or None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plugins-root", default=str(ROOT / "plugins"))
    parser.add_argument("--cases", default=str(ROOT / "tests" / "evals" / "routing.json"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--model", default=None)
    parser.add_argument("--out", default=None, help="write the full report as JSON")
    args = parser.parse_args()

    if not shutil.which("claude"):
        sys.exit("The Claude Code CLI (claude) is not installed.")
    plugins_root = Path(args.plugins_root).resolve()
    plugin_dirs = sorted(p for p in plugins_root.iterdir() if (p / ".claude-plugin" / "plugin.json").exists())
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]

    jobs = [(i, run) for i in range(len(cases)) for run in range(args.runs)]
    results = {i: [] for i in range(len(cases))}
    with tempfile.TemporaryDirectory(prefix="god-mode-eval-") as home, \
            ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(first_skill_call, cases[i]["query"], plugin_dirs, Path(home), args.model,
                               args.timeout): i for i, _ in jobs}
        for fut in as_completed(futures):
            results[futures[fut]].append(fut.result())

    report, passed, total, errors = [], 0, 0, 0
    by_plugin = {}
    for i, case in enumerate(cases):
        expected = case["expected"] if isinstance(case["expected"], list) else [case["expected"]]
        valid = [r for r in results[i] if r != ERROR]
        errors += len(results[i]) - len(valid)
        hits = sum(1 for r in valid if r in expected)
        passed += hits
        total += len(valid)
        stats = by_plugin.setdefault(case["plugin"], [0, 0])
        stats[0] += hits
        stats[1] += len(valid)
        report.append({**case, "picked": results[i], "hits": hits})
        mark = "ok  " if valid and hits == len(valid) else ("ERR " if not valid else "FAIL")
        print(f"{mark} [{case['plugin']}] {case['query'][:70]!r} -> {results[i]} (esperado {expected})")

    print()
    for plugin, (h, t) in sorted(by_plugin.items()):
        print(f"{plugin}: {h}/{t}")
    print(f"Total: {passed}/{total} ({100 * passed / max(1, total):.0f}%)" + (f", {errors} runs failed" if errors else ""))
    if args.out:
        Path(args.out).write_text(json.dumps({"passed": passed, "total": total, "errors": errors, "by_plugin": by_plugin,
                                              "cases": report}, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
