import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "god-mode-core" / "hooks" / "prompt_audit_check.py"


class PromptAuditCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.home = base / "home"
        self.project = base / "home" / "work" / "app"
        (self.home / ".claude" / "skills" / "demo").mkdir(parents=True)
        (self.home / ".claude" / "skills" / "demo" / "SKILL.md").write_text("---\nname: demo\n---\n", encoding="utf-8")
        (self.home / ".claude" / "CLAUDE.md").write_text("global\n", encoding="utf-8")
        (self.project / "api").mkdir(parents=True)
        (self.project / "CLAUDE.md").write_text("project\n", encoding="utf-8")
        (self.project / "api" / "AGENTS.md").write_text("nested\n", encoding="utf-8")
        (self.project / "node_modules" / "pkg").mkdir(parents=True)
        (self.project / "node_modules" / "pkg" / "CLAUDE.md").write_text("ignored\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, source="compact", session="s1", mode=None, model="claude-fable-5-1"):
        env = {k: v for k, v in os.environ.items() if k not in ("GOD_MODE_PROMPT_AUDIT", "CLAUDE_PROJECT_DIR")}
        env["HOME"] = str(self.home)
        if mode:
            env["GOD_MODE_PROMPT_AUDIT"] = mode
        payload = json.dumps({"source": source, "session_id": session, "cwd": str(self.project), "model": model})
        out = subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True,
                             env=env, check=True)
        return out.stdout

    def touch(self, path):
        later = time.time() + 5
        os.utime(path, (later, later))

    def test_first_compaction_asks_for_the_audit_with_the_session_model(self):
        out = self.run_hook()
        self.assertIn("Es el primer audit de este proyecto", out)
        self.assertIn('model: "fable"', out)
        self.assertIn("4 archivos", out)
        self.assertIn("`prompt-audit`", out)

    def test_no_audit_when_nothing_changed(self):
        self.run_hook(session="s1")
        self.assertEqual(self.run_hook(session="s2"), "")

    def test_changed_nested_file_triggers_again(self):
        self.run_hook(session="s1")
        self.touch(self.project / "api" / "AGENTS.md")
        self.assertIn("cambiaron desde el último audit", self.run_hook(session="s2"))

    def test_changed_global_skill_triggers_again(self):
        self.run_hook(session="s1")
        self.touch(self.home / ".claude" / "skills" / "demo" / "SKILL.md")
        self.assertIn("cambiaron", self.run_hook(session="s2"))

    def test_ignored_folders_do_not_count(self):
        self.run_hook(session="s1")
        self.touch(self.project / "node_modules" / "pkg" / "CLAUDE.md")
        self.assertEqual(self.run_hook(session="s2"), "")

    def test_second_hook_for_the_same_compaction_stays_quiet(self):
        self.assertNotEqual(self.run_hook(session="s1", mode="always"), "")
        self.assertEqual(self.run_hook(session="s1", mode="always"), "")

    def test_always_and_off(self):
        self.run_hook(session="s1")
        self.assertNotEqual(self.run_hook(session="s2", mode="always"), "")
        self.touch(self.project / "CLAUDE.md")
        self.assertEqual(self.run_hook(session="s3", mode="off"), "")

    def test_only_compactions(self):
        self.assertEqual(self.run_hook(source="startup"), "")
        self.assertEqual(self.run_hook(source="resume"), "")

    def test_unknown_model_still_asks_for_the_same_model(self):
        out = self.run_hook(model=None)
        self.assertIn("el mismo modelo de esta sesión", out)
        self.assertNotIn('model: "', out)


if __name__ == "__main__":
    unittest.main()
