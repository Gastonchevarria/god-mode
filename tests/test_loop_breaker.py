import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "god-mode-core" / "hooks" / "loop_breaker.py"


class LoopBreakerTest(unittest.TestCase):
    def tearDown(self):
        self.tmp.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.calls = 0

    def run_hook(self, command, session="s1", tool="Bash", limit=None, raw=None, call_id=None):
        env = {k: v for k, v in os.environ.items() if k != "GOD_MODE_LOOP_MAX"}
        env["TMPDIR"] = self.tmp.name
        if limit is not None:
            env["GOD_MODE_LOOP_MAX"] = str(limit)
        self.calls += 1
        payload = raw if raw is not None else json.dumps(
            {"session_id": session, "hook_event_name": "PreToolUse", "tool_name": tool,
             "tool_use_id": call_id or f"toolu_{self.calls}", "tool_input": {"command": command}})
        return subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True, env=env, check=False)

    def test_the_fourth_identical_command_in_a_row_is_blocked(self):
        for _ in range(3):
            self.assertEqual(self.run_hook("pytest tests/").returncode, 0)
        r = self.run_hook("pytest tests/")
        self.assertEqual(r.returncode, 2)
        self.assertIn("3 veces seguidas", r.stderr)
        self.assertIn("pytest tests/", r.stderr)

    def test_a_different_command_in_between_resets_the_count(self):
        for _ in range(3):
            self.run_hook("pytest tests/")
        self.assertEqual(self.run_hook("git diff --stat").returncode, 0)
        self.assertEqual(self.run_hook("pytest tests/").returncode, 0)

    def test_a_sleep_before_the_retry_does_not_hide_the_loop(self):
        self.run_hook("curl -s https://api.example.com/health")
        self.run_hook("sleep 30 && curl -s https://api.example.com/health")
        self.run_hook("sleep 60; curl -s   https://api.example.com/health")
        self.assertEqual(self.run_hook("curl -s https://api.example.com/health").returncode, 2)

    def test_it_stays_blocked_until_something_else_runs(self):
        for _ in range(4):
            self.run_hook("npm test")
        self.assertEqual(self.run_hook("npm test").returncode, 2)

    def test_sessions_do_not_share_counts(self):
        for _ in range(3):
            self.run_hook("pytest", session="a")
        self.assertEqual(self.run_hook("pytest", session="b").returncode, 0)

    def test_the_limit_is_configurable_and_zero_turns_it_off(self):
        self.run_hook("make", limit=1)
        self.assertEqual(self.run_hook("make", limit=1).returncode, 2)
        for _ in range(6):
            self.assertEqual(self.run_hook("make", session="off", limit=0).returncode, 0)

    def test_the_same_call_seen_twice_at_once_counts_once(self):
        # god-mode loaded as a plugin and from the installer runs the hook twice per command
        for i in range(3):
            self.assertEqual(self.run_hook("pytest tests/", call_id=f"toolu_same_{i}").returncode, 0)
            self.assertEqual(self.run_hook("pytest tests/", call_id=f"toolu_same_{i}").returncode, 0)
        self.assertEqual(self.run_hook("pytest tests/").returncode, 2)

    def test_other_tools_and_bad_input_never_block(self):
        for _ in range(5):
            self.assertEqual(self.run_hook("x", tool="Read").returncode, 0)
        self.assertEqual(self.run_hook(None, raw="not json").returncode, 0)
        self.assertEqual(self.run_hook(None, raw="{}").returncode, 0)


if __name__ == "__main__":
    unittest.main()
