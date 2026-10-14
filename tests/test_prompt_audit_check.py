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
        self.linked = base / "god-mode" / "skills" / "linked"
        self.linked.mkdir(parents=True)
        (self.linked / "SKILL.md").write_text("---\nname: linked\n---\n", encoding="utf-8")
        (self.home / ".claude" / "skills" / "linked").symlink_to(self.linked, target_is_directory=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, source="compact", session="s1", mode=None, model="claude-fable-5-1", max_kb=None):
        env = {k: v for k, v in os.environ.items()
               if k not in ("GOD_MODE_PROMPT_AUDIT", "GOD_MODE_PROMPT_AUDIT_MAX_KB", "CLAUDE_PROJECT_DIR")}
        env["HOME"] = str(self.home)
        if mode:
            env["GOD_MODE_PROMPT_AUDIT"] = mode
        if max_kb is not None:
            env["GOD_MODE_PROMPT_AUDIT_MAX_KB"] = str(max_kb)
        payload = json.dumps({"source": source, "session_id": session, "cwd": str(self.project), "model": model})
        out = subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True,
                             env=env, check=True)
        return out.stdout

    def touch(self, path):
        later = time.time() + 5
        os.utime(path, (later, later))

    def test_first_compaction_audits_on_sonnet_for_the_session_model(self):
        out = self.run_hook()
        self.assertIn("Es el primer audit de este proyecto", out)
        self.assertIn('model: "sonnet"', out)
        self.assertIn("`claude-fable-5-1` como modelo destino", out)
        self.assertIn("4 archivos", out)
        self.assertIn("`prompt-audit`", out)
        self.assertIn("- api/AGENTS.md", out)
        self.assertIn("- ~/.claude/CLAUDE.md", out)

    def test_no_audit_when_nothing_changed(self):
        self.run_hook(session="s1")
        self.assertEqual(self.run_hook(session="s2"), "")

    def test_only_the_changed_file_is_audited(self):
        self.run_hook(session="s1")
        self.touch(self.project / "api" / "AGENTS.md")
        out = self.run_hook(session="s2")
        self.assertIn("Cambiaron instrucciones desde el último audit", out)
        self.assertIn("1 archivo (", out)
        self.assertIn("- api/AGENTS.md", out)
        self.assertNotIn("- CLAUDE.md", out)

    def test_changed_global_skill_triggers_again(self):
        self.run_hook(session="s1")
        self.touch(self.home / ".claude" / "skills" / "demo" / "SKILL.md")
        self.assertIn("- ~/.claude/skills/demo/SKILL.md", self.run_hook(session="s2"))

    def test_linked_skills_are_left_out(self):
        self.assertNotIn("linked", self.run_hook(session="s1"))
        self.touch(self.linked / "SKILL.md")
        self.assertEqual(self.run_hook(session="s2"), "")

    def test_ignored_folders_do_not_count(self):
        self.run_hook(session="s1")
        self.touch(self.project / "node_modules" / "pkg" / "CLAUDE.md")
        self.assertEqual(self.run_hook(session="s2"), "")

    def test_large_change_is_offered_not_run(self):
        self.run_hook(session="s1")
        (self.project / "CLAUDE.md").write_text("x" * 3000, encoding="utf-8")
        out = self.run_hook(session="s2", max_kb=2)
        self.assertIn("no corre solo", out)
        self.assertIn("- CLAUDE.md", out)
        self.assertNotIn("Lanzá un subagente", out)
        self.assertEqual(self.run_hook(session="s3", max_kb=2), "")

    def test_state_from_older_versions_becomes_the_baseline(self):
        state = self.home / ".claude" / ".god-mode-prompt-audit.json"
        state.write_text(json.dumps({"projects": {str(self.project.resolve()): {"fingerprint": "abc", "files": 4}}}),
                         encoding="utf-8")
        self.assertEqual(self.run_hook(session="s1"), "")
        self.touch(self.project / "CLAUDE.md")
        self.assertIn("- CLAUDE.md", self.run_hook(session="s2"))

    def test_second_hook_for_the_same_compaction_stays_quiet(self):
        self.assertNotEqual(self.run_hook(session="s1", mode="always"), "")
        self.assertEqual(self.run_hook(session="s1", mode="always"), "")

    def test_always_and_off(self):
        self.run_hook(session="s1")
        self.assertIn("4 archivos", self.run_hook(session="s2", mode="always"))
        self.touch(self.project / "CLAUDE.md")
        self.assertEqual(self.run_hook(session="s3", mode="off"), "")

    def test_only_compactions(self):
        self.assertEqual(self.run_hook(source="startup"), "")
        self.assertEqual(self.run_hook(source="resume"), "")

    def test_unknown_model_targets_the_session_model(self):
        out = self.run_hook(model=None)
        self.assertIn("con el modelo de esta sesión como modelo destino", out)
        self.assertIn('model: "sonnet"', out)


if __name__ == "__main__":
    unittest.main()
