import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "god-mode-core" / "hooks" / "blast_radius.py"


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


class BlastRadiusTest(unittest.TestCase):
    def setUp(self):
        # Outside the system temp dir on purpose: the hook treats temp dirs as a free zone.
        self.tmp = tempfile.TemporaryDirectory(dir=Path.home())
        self.scratch = Path(self.tmp.name) / "tmpdir"
        self.scratch.mkdir()
        self.project = Path(self.tmp.name) / "proyecto"
        self.project.mkdir()
        git(self.project, "init", "-q", "-b", "main")
        (self.project / "a.py").write_text("print(1)\n")
        (self.project / "b.py").write_text("print(2)\n")
        git(self.project, "add", ".")
        git(self.project, "commit", "-qm", "base")

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, tool, tool_input, cwd=None, env_extra=None, raw=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GOD_MODE_")}
        env["TMPDIR"] = str(self.scratch)
        env.update(env_extra or {})
        payload = raw if raw is not None else json.dumps(
            {"session_id": "s1", "cwd": str(cwd or self.project), "hook_event_name": "PreToolUse",
             "tool_name": tool, "tool_use_id": "toolu_1", "tool_input": tool_input})
        return subprocess.run([sys.executable, str(SCRIPT)], input=payload, capture_output=True, text=True,
                              env=env, check=False)

    # --- comandos destructivos en Bash ---

    def test_git_reset_hard_is_blocked_and_lists_the_changes_it_would_discard(self):
        (self.project / "a.py").write_text("print(3)\n")
        (self.project / "nuevo.py").write_text("x\n")
        r = self.run_hook("Bash", {"command": "git reset --hard HEAD"})
        self.assertEqual(r.returncode, 2)
        self.assertIn("a.py", r.stderr)
        self.assertIn("nuevo.py", r.stderr)
        self.assertIn("2 archivos", r.stderr)

    def test_git_checkout_and_restore_discards_are_blocked(self):
        (self.project / "a.py").write_text("print(3)\n")
        for cmd in ("git checkout -- .", "git checkout -- a.py", "git restore a.py", "git clean -fd", "git stash drop"):
            self.assertEqual(self.run_hook("Bash", {"command": cmd}).returncode, 2, cmd)

    def test_git_restore_staged_and_a_clean_tree_pass(self):
        self.assertEqual(self.run_hook("Bash", {"command": "git restore --staged a.py"}).returncode, 0)
        self.assertEqual(self.run_hook("Bash", {"command": "git reset --hard HEAD"}).returncode, 0)

    def test_force_push_is_blocked_with_the_branch_named(self):
        for cmd in ("git push --force origin main", "git push -f", "git push origin +main"):
            r = self.run_hook("Bash", {"command": cmd})
            self.assertEqual(r.returncode, 2, cmd)
        self.assertIn("main", r.stderr)

    def test_rm_outside_tmp_is_blocked_with_a_count_and_a_way_out(self):
        (self.project / "dir").mkdir()
        (self.project / "dir" / "x.txt").write_text("x")
        (self.project / "dir" / "y.txt").write_text("y")
        r = self.run_hook("Bash", {"command": "rm -rf dir a.py"})
        self.assertEqual(r.returncode, 2)
        self.assertIn("3 archivos", r.stderr)
        self.assertIn("_to_delete/", r.stderr)

    def test_rm_inside_tmp_passes(self):
        self.assertEqual(self.run_hook("Bash", {"command": f"rm -rf {self.scratch}/corrida"}).returncode, 0)
        self.assertEqual(self.run_hook("Bash", {"command": "rm -f /tmp/salida.log"}).returncode, 0)

    def test_ordinary_commands_pass(self):
        for cmd in ("git status", "git push origin main", "ls -la", "rm -h", "python3 -m unittest", "git stash list"):
            self.assertEqual(self.run_hook("Bash", {"command": cmd}).returncode, 0, cmd)

    # --- escrituras fuera del proyecto ---

    def test_writing_outside_the_project_is_blocked(self):
        other = Path(self.tmp.name) / "otro-proyecto" / "notas.md"
        for tool, key in (("Write", "file_path"), ("Edit", "file_path"), ("MultiEdit", "file_path"),
                          ("NotebookEdit", "notebook_path")):
            r = self.run_hook(tool, {key: str(other)})
            self.assertEqual(r.returncode, 2, tool)
            self.assertIn("fuera", r.stderr)

    def test_writing_inside_the_project_tmp_and_claude_dir_passes(self):
        home = Path(self.tmp.name) / "home"
        (home / ".claude").mkdir(parents=True)
        self.assertEqual(self.run_hook("Write", {"file_path": str(self.project / "src" / "c.py")}).returncode, 0)
        self.assertEqual(self.run_hook("Write", {"file_path": "/tmp/scratch/x.md"}).returncode, 0)
        self.assertEqual(self.run_hook("Write", {"file_path": f"{self.scratch}/x.md"}).returncode, 0)
        self.assertEqual(self.run_hook("Write", {"file_path": str(home / ".claude" / "x.md")},
                                       env_extra={"HOME": str(home)}).returncode, 0)

    def test_a_relative_path_is_resolved_against_cwd(self):
        self.assertEqual(self.run_hook("Write", {"file_path": "docs/x.md"}).returncode, 0)
        self.assertEqual(self.run_hook("Write", {"file_path": "../otro/x.md"}).returncode, 2)

    # --- desactivación y robustez ---

    def test_off_switch_and_bad_input_never_block(self):
        (self.project / "a.py").write_text("print(3)\n")
        self.assertEqual(self.run_hook("Bash", {"command": "git reset --hard"}, env_extra={"GOD_MODE_BLAST": "off"}).returncode, 0)
        self.assertEqual(self.run_hook("Read", {"file_path": "/etc/hosts"}).returncode, 0)
        self.assertEqual(self.run_hook(None, None, raw="not json").returncode, 0)
        self.assertEqual(self.run_hook(None, None, raw="{}").returncode, 0)


if __name__ == "__main__":
    unittest.main()
