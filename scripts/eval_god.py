#!/usr/bin/env python3
"""
/god route evaluation: which route does /god pick, and what does it load to get there?

Sends each request as `/god-mode-core:god <request>` with the plugins loaded in an isolated
HOME, stops after a few turns, and records:

- the route named on the `⚡ GOD · Ruta: ...` line;
- the skills /god loads (Skill tool calls), which cost context;
- whether it read references/protocol.md, which the session already carries;
- the cost of those first turns.

A case passes when its expected route token (for example `DEBUG` or `DIRECT`) appears in
the route /god names. The other numbers are reported, not scored.

Usage:
    python3 scripts/eval_god.py [--cases tests/evals/god_routes.json] [--runs 1]
                                [--model claude-fable-5-1] [--out report.json]

Requires the Claude Code CLI (`claude`) with working authentication.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_routing import ROOT, isolated_env  # noqa: E402

ROUTE_RE = re.compile(r"(?:Ruta|Route):\s*(.+?)\s*(?:·|\n|$)")


def normalize(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[*`_\[\]]", "", text).strip().upper()


def run_case(query, plugin_dirs, home, model, max_turns, timeout):
    cmd = ["claude", "-p", f"/god-mode-core:god {query}", "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns)]
    for d in plugin_dirs:
        cmd += ["--plugin-dir", str(d)]
    if model:
        cmd += ["--model", model]
    workdir = tempfile.mkdtemp(dir=home)
    run = {"route": None, "skills": [], "tools": [], "protocol_reads": 0, "cost_usd": None, "error": None}
    texts = []
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=isolated_env(home), cwd=workdir,
                              timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        run["error"] = "timeout"
    else:
        output = proc.stdout
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "text":
                    texts.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    tool_input = block.get("input", {})
                    run["tools"].append(block.get("name"))
                    if block.get("name") == "Skill":
                        name = tool_input.get("skill", "").split(":", 1)[-1].lstrip("/")
                        if name and name != "god":
                            run["skills"].append(name)
                    elif block.get("name") == "Read" and \
                            tool_input.get("file_path", "").endswith("references/protocol.md"):
                        run["protocol_reads"] += 1
        elif event.get("type") == "result":
            run["cost_usd"] = event.get("total_cost_usd")
            if event.get("is_error") and event.get("subtype") == "success":
                run["error"] = str(event.get("result", "error"))[:80]
    run["first_text"] = next((t.strip()[:160] for t in texts if t.strip()), "")
    match = ROUTE_RE.search("\n".join(texts))
    if match:
        run["route"] = normalize(match.group(1))
    elif run["error"] is None:
        run["error"] = "no route line"
    return run


DIRECT_ALIASES = ("DIRECT", "NINGUNA", "NONE")


def route_matches(expected, route, known):
    """The route's name, before any parenthesis, names the expected route and no other one."""
    head = route.split("(")[0]
    if expected == "DIRECT":
        return any(alias in head for alias in DIRECT_ALIASES) and not any(k in head for k in known)
    return expected in head and not any(k in head for k in known if k != expected and k not in expected)


def summarize(cases, results, max_turns, model, out):
    known = {normalize(c["route"]) for c in cases} - {"DIRECT"}
    report, hits, scored, skills, protocol_reads, cost = [], 0, 0, 0, 0, 0.0
    for i, case in enumerate(cases):
        expected = normalize(case["route"])
        runs = results[i]
        ok = [r for r in runs if r["route"] and route_matches(expected, r["route"], known)]
        valid = [r for r in runs if r["route"]]
        hits += len(ok)
        scored += len(runs)
        skills += sum(len(r["skills"]) for r in runs)
        protocol_reads += sum(r["protocol_reads"] for r in runs)
        cost += sum(r["cost_usd"] or 0 for r in runs)
        report.append({**case, "runs": runs, "hits": len(ok)})
        mark = "ok  " if len(ok) == len(runs) else ("ERR " if not valid else "FAIL")
        picked = [f"{r['route'] or r['error']} {r['skills']}" for r in runs]
        print(f"{mark} [{case['route']}] {case['query'][:60]!r} -> {picked}")

    runs_total = max(1, scored)
    print()
    print(f"Rutas correctas: {hits}/{scored} ({100 * hits / runs_total:.0f}%)")
    print(f"Skills cargadas por corrida: {skills / runs_total:.1f}")
    print(f"Lecturas de protocol.md: {protocol_reads} en {scored} corridas")
    print(f"Costo de los primeros {max_turns} turnos: US$ {cost:.2f} en total, US$ {cost / runs_total:.3f} por corrida")
    if out:
        Path(out).write_text(json.dumps({
            "passed": hits, "total": scored, "skills_per_run": skills / runs_total,
            "protocol_reads": protocol_reads, "cost_usd": cost, "max_turns": max_turns,
            "model": model, "cases": report}, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plugins-root", default=str(ROOT / "plugins"))
    parser.add_argument("--cases", default=str(ROOT / "tests" / "evals" / "god_routes.json"))
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--max-turns", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--model", default=None)
    parser.add_argument("--out", default=None, help="write the full report as JSON")
    parser.add_argument("--rescore", default=None, help="score an earlier --out report again, without running")
    args = parser.parse_args()

    if args.rescore:
        old = json.loads(Path(args.rescore).read_text(encoding="utf-8"))
        cases = [{k: v for k, v in c.items() if k not in ("runs", "hits")} for c in old["cases"]]
        summarize(cases, {i: c["runs"] for i, c in enumerate(old["cases"])}, old["max_turns"], old["model"], args.out)
        return 0

    if not shutil.which("claude"):
        sys.exit("The Claude Code CLI (claude) is not installed.")
    plugins_root = Path(args.plugins_root).resolve()
    plugin_dirs = sorted(p for p in plugins_root.iterdir() if (p / ".claude-plugin" / "plugin.json").exists())
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]

    results = {i: [] for i in range(len(cases))}
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="god-mode-god-eval-") as home, \
            ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run_case, cases[i]["query"], plugin_dirs, Path(home), args.model,
                               args.max_turns, args.timeout): i
                   for i in range(len(cases)) for _ in range(args.runs)}
        for fut in as_completed(futures):
            results[futures[fut]].append(fut.result())
    summarize(cases, results, args.max_turns, args.model, args.out)
    print(f"Tiempo: {time.time() - started:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
