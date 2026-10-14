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


def assistant(msg_id, read, write=0, content=None):
    return {"type": "assistant", "message": {"id": msg_id, "model": "claude-opus-5-5", "content": content or [],
                                             "usage": {"input_tokens": 10, "cache_creation_input_tokens": write,
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
        second = next(line for line in out.splitlines() if "$0.25" in line)
        self.assertIn(" -p ", second)
        self.assertIn("Total: $12.75", out)
        self.assertIn("claude-opus-5-5 $12.00", out)
        self.assertIn("1 sesión pasó los 300k tokens", out)
        self.assertIn("1 audit de instrucciones", out)
        self.assertIn("1 sesión de `claude -p`", out)

    def test_old_sessions_are_left_out(self):
        path = self.session("-p", "old", [assistant("m1", 5)])
        os.utime(path, (1_000_000, 1_000_000))
        self.assertIn("No hay sesiones", self.run_usage("--days=1"))


if __name__ == "__main__":
    unittest.main()
