import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "bin" / "god-mode"


def assistant(msg_id, read, write=0, content=None, ttl="5m"):
    return {"type": "assistant", "message": {"id": msg_id, "model": "claude-opus-5-5", "content": content or [],
                                             "usage": {"input_tokens": 10, "cache_creation_input_tokens": write,
                                                       "cache_creation": {f"ephemeral_{ttl}_input_tokens": write},
                                                       "cache_read_input_tokens": read, "output_tokens": 50}}}


def tool_use(name, args):
    return [{"type": "tool_use", "id": "t", "name": name, "input": args}]


class UsageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.projects = self.home / ".claude" / "projects"

    def tearDown(self):
        self.tmp.cleanup()

    def session(self, folder, sid, rows, subagents=None):
        path = self.projects / folder / f"{sid}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
        for name, sub_rows in (subagents or {}).items():
            sub = path.with_suffix("") / "subagents" / f"{name}.jsonl"
            sub.parent.mkdir(parents=True, exist_ok=True)
            sub.write_text("\n".join(json.dumps(r) for r in sub_rows) + "\n", encoding="utf-8")
        return path

    def run_usage(self, *args):
        env = dict(os.environ, HOME=str(self.home))
        out = subprocess.run([sys.executable, str(CLI), "usage", *args], capture_output=True, text=True, env=env,
                             check=True).stdout
        return re.sub(r"\x1b\[[0-9;]*m", "", out)

    def test_reports_cost_context_compactions_and_agents(self):
        self.session("-Users-me-Billetera", "s1", [
            {"type": "user", "cwd": "/Users/me/Billetera", "entrypoint": "cli", "message": {"content": "hola"}},
            assistant("m1", 20_000, 5_000, tool_use("Skill", {"skill": "graphify"})),
            assistant("m1", 20_000, 5_000),
            assistant("m2", 440_000, 0, tool_use("Agent", {"prompt": "cargá claude-api con prompt-audit"})),
            {"type": "system", "subtype": "compact_boundary", "compactMetadata": {"preTokens": 450_000}},
            {"type": "cost-state", "totalCostUSD": 12.5,
             "modelUsage": {"claude-opus-5-5": {"costUSD": 12.0, "cacheReadInputTokens": 1_000},
                            "claude-sonnet-5-5": {"costUSD": 0.5}}},
        ], subagents={"agent-a": [assistant("x1", 30_000)]})
        self.session("-Users-me-Billetera", "s2", [
            {"type": "user", "cwd": "/Users/me/Billetera", "entrypoint": "sdk-cli", "message": {"content": "reflect"}},
            assistant("r1", 1_000),
            {"type": "cost-state", "totalCostUSD": 0.25, "modelUsage": {"claude-haiku-4-5": {"costUSD": 0.25}}},
        ])
        out = self.run_usage("--days", "1")
        first = next(line for line in out.splitlines() if "$12.50" in line)
        self.assertIn("Billetera", first)
        self.assertIn("490k", first)  # cache reads: 20k (once) + 440k + 30k from the subagent
        self.assertIn("450k", first)  # largest context, from the compaction
        self.assertIn("graphify×1", first)
        self.assertIn("opus-5-5", first)
        second = next(line for line in out.splitlines() if "$0.25" in line)
        self.assertIn("haiku-4-5 -p", second)
        self.assertIn("Total: $12.75", out)
        self.assertIn("claude-opus-5-5 $12.00", out)
        self.assertIn("1 sesión pasó los 300k tokens", out)
        self.assertIn("1 audit de instrucciones", out)
        self.assertIn("1 sesión de `claude -p`", out)

    def test_empty_sessions_are_hidden(self):
        self.session("-Users-me-app", "busy", [{"type": "user", "cwd": "/Users/me/app"}, assistant("m1", 1_000)])
        self.session("-Users-me-app", "empty", [{"type": "user", "cwd": "/Users/me/app"},
                                                {"type": "cost-state", "totalCostUSD": 0, "modelUsage": {}}])
        out = self.run_usage()
        self.assertIn("(1 sesión, 1 vacía sin mostrar", out)
        self.assertNotIn("$0.00", out)

    def test_graph_that_was_never_queried_is_reported(self):
        queried, idle = self.home / "queried", self.home / "idle"
        for repo in (queried, idle):
            (repo / "graphify-out" / "cache").mkdir(parents=True)
            (repo / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
            self.session(f"-{repo.name}", repo.name, [{"type": "user", "cwd": str(repo)}, assistant("m1", 1_000)])
        (queried / "graphify-out" / "cache" / "last_query_stamp").write_text("1", encoding="utf-8")
        out = self.run_usage()
        self.assertIn("Graphify: idle tiene grafo y Claude no lo consultó", out)
        self.assertNotIn("queried tiene", out)

    def test_expired_cache_is_reported_with_its_ttl(self):
        rows = [{"type": "user", "cwd": "/Users/me/app"}, assistant("m1", 0, 40_000), assistant("m2", 40_000, 30_000),
                assistant("m3", 1_000, 90_000), assistant("m4", 91_000, 2_000)]
        self.session("-Users-me-app", "s5m", rows)
        out = self.run_usage()
        self.assertIn("1 vez la caché estaba vencida", out)
        self.assertIn("90k tokens", out)
        self.assertIn("ENABLE_PROMPT_CACHING_1H=1", out)

    def test_one_hour_cache_is_recognized(self):
        self.session("-Users-me-app", "s1h", [{"type": "user", "cwd": "/Users/me/app"},
                                              assistant("m1", 0, 80_000, ttl="1h"), assistant("m2", 1_000, 90_000, ttl="1h")])
        self.assertIn("La caché ya dura 1 hora", self.run_usage())

    def test_old_sessions_are_left_out(self):
        path = self.session("-p", "old", [assistant("m1", 5)])
        os.utime(path, (1_000_000, 1_000_000))
        self.assertIn("No hay sesiones", self.run_usage("--days=1"))


if __name__ == "__main__":
    unittest.main()
