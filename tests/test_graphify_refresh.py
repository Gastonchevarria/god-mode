import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "god-mode-core" / "hooks" / "graphify_refresh.py"
FAKE = """#!/bin/sh
echo "$PWD $* $PYTHONHASHSEED" >> "{log}"
"""


class GraphifyRefreshTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.home = base / "home"
        self.bin = base / "bin"
        self.project = base / "repo"
        self.log = base / "calls.log"
        for d in (self.home, self.bin, self.project / "graphify-out"):
            d.mkdir(parents=True)
        (self.project / "graphify-out" / "graph.json").write_text("{}", encoding="utf-8")
        self.fake(self.bin / "graphify")

    def tearDown(self):
        self.tmp.cleanup()

    def fake(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(FAKE.format(log=self.log), encoding="utf-8")
        path.chmod(0o755)

    def run_hook(self, source="compact", path=None, mode=None, project=None):
        env = {k: v for k, v in os.environ.items() if k not in ("GOD_MODE_GRAPHIFY_REFRESH", "CLAUDE_PROJECT_DIR")}
        env["HOME"] = str(self.home)
        env["PATH"] = f"{path or self.bin}:/usr/bin:/bin"
        if mode:
            env["GOD_MODE_GRAPHIFY_REFRESH"] = mode
        payload = json.dumps({"source": source, "cwd": str(project or self.project)})
        out = subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True, env=env,
                             check=True)
        return out.stdout

    def calls(self, wait=True):
        deadline = time.time() + (3 if wait else 0.3)
        while time.time() < deadline:
            if self.log.exists() and self.log.read_text().strip():
                return self.log.read_text().splitlines()
            time.sleep(0.05)
        return []

    def test_compaction_updates_the_graph_quietly(self):
        self.assertEqual(self.run_hook("compact"), "")
        self.assertEqual(self.calls(), [f"{self.project.resolve()} update . 0"])

    def test_session_start_updates_too(self):
        self.run_hook("startup")
        self.assertEqual(len(self.calls()), 1)

    def test_resume_and_clear_do_not(self):
        self.run_hook("resume")
        self.run_hook("clear")
        self.assertEqual(self.calls(wait=False), [])

    def test_project_without_graph_is_left_alone(self):
        other = Path(self.tmp.name) / "other"
        other.mkdir()
        self.run_hook(project=other)
        self.assertEqual(self.calls(wait=False), [])

    def test_off(self):
        self.run_hook(mode="off")
        self.assertEqual(self.calls(wait=False), [])

    def test_finds_graphify_in_local_bin_when_path_lacks_it(self):
        self.fake(self.home / ".local" / "bin" / "graphify")
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        self.run_hook(path=empty)
        self.assertEqual(len(self.calls()), 1)

    def test_no_cli_no_error(self):
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        self.assertEqual(self.run_hook(path=empty), "")
        self.assertEqual(self.calls(wait=False), [])


if __name__ == "__main__":
    unittest.main()
