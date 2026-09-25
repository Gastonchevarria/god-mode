import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("install_skill", ROOT / "scripts" / "install-skill.py")
install_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(install_skill)

POC_URL = "https://github.com/owner/repo/tree/main;echo${IFS}INYECTADO>PRUEBA_POC.txt;/skills/x"


def make_skill(root, name="demo-skill"):
    skill_dir = Path(root) / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(f"---\nname: {name}\ndescription: demo\n---\n# Demo\n", encoding="utf-8")
    return skill_dir


class IsolatedHomeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.claude = base / "home" / ".claude" / "skills"
        self.gemini = base / "home" / ".gemini" / "config" / "skills"
        self.src = base / "src"
        self.src.mkdir()
        patches = [
            mock.patch.object(install_skill, "CLAUDE_SKILLS", self.claude),
            mock.patch.object(install_skill, "GEMINI_SKILLS", self.gemini),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def tearDown(self):
        self.tmp.cleanup()


class ParseGithubUrlTest(unittest.TestCase):
    def test_poc_injection_url_is_rejected(self):
        with self.assertRaises(install_skill.UnsafeInputError):
            install_skill.parse_github_url(POC_URL)

    def test_shell_metacharacters_in_every_component_are_rejected(self):
        for url in [
            "https://github.com/own;er/repo",
            "https://github.com/owner/re$(id)po",
            "https://github.com/owner/repo/tree/ma`id`in/skills/x",
            "https://github.com/owner/repo/tree/main/skills/x;id",
            "https://github.com/owner/repo/tree/-upload-pack=x/skills",
        ]:
            with self.subTest(url=url), self.assertRaises(install_skill.UnsafeInputError):
                install_skill.parse_github_url(url)

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(install_skill.UnsafeInputError):
            install_skill.parse_github_url("https://github.com/owner/repo/tree/main/../../etc")

    def test_valid_urls_parse(self):
        tree = install_skill.parse_github_url("https://github.com/owner/repo/tree/main/skills/foo")
        self.assertEqual(
            (tree["owner"], tree["repo"], tree["branch"], tree["subpath"]),
            ("owner", "repo", "main", "skills/foo"),
        )
        blob = install_skill.parse_github_url("https://github.com/owner/repo/blob/main/skills/foo/SKILL.md")
        self.assertEqual(blob["subpath"], "skills/foo")
        root_blob = install_skill.parse_github_url("https://github.com/owner/repo/blob/main/SKILL.md")
        self.assertIsNone(root_blob["subpath"])
        short = install_skill.parse_github_url("owner/repo")
        self.assertEqual(short["clone_url"], "https://github.com/owner/repo.git")
        dotgit = install_skill.parse_github_url("https://github.com/owner/repo.git")
        self.assertEqual(dotgit["repo"], "repo")

    def test_unknown_format_returns_none(self):
        self.assertIsNone(install_skill.parse_github_url("https://gitlab.com/owner/repo"))
        self.assertIsNone(install_skill.parse_github_url("http://github.com/owner/repo"))


class CloneCommandTest(unittest.TestCase):
    def test_clone_command_is_an_argument_list(self):
        info = install_skill.parse_github_url("https://github.com/owner/repo/tree/dev/skills/foo")
        self.assertEqual(
            install_skill.build_clone_cmd(info),
            ["git", "clone", "--depth", "1", "--branch", "dev", "--", "https://github.com/owner/repo.git", "repo"],
        )

    def test_run_cmd_refuses_shell_strings(self):
        with self.assertRaises(TypeError):
            install_skill.run_cmd("git clone x")


class InstallFromGithubTest(unittest.TestCase):
    def test_poc_url_runs_nothing_and_creates_no_file(self):
        with tempfile.TemporaryDirectory() as cwd:
            previous = os.getcwd()
            os.chdir(cwd)
            try:
                with mock.patch.object(subprocess, "run") as run, redirect_stdout(io.StringIO()):
                    ok = install_skill.install_from_github(POC_URL)
            finally:
                os.chdir(previous)
            self.assertFalse(ok)
            run.assert_not_called()
            self.assertEqual(os.listdir(cwd), [])

    def test_missing_subpath_does_not_install_whole_repo(self):
        def fake_clone(args, cwd=None):
            repo = Path(cwd) / "repo"
            make_skill(repo / "skills", "other-skill")
            return True, "", ""

        with mock.patch.object(install_skill, "run_cmd", side_effect=fake_clone), \
                mock.patch.object(install_skill, "install_skill_directory") as install_dir, \
                redirect_stdout(io.StringIO()):
            ok = install_skill.install_from_github("https://github.com/owner/repo/tree/main/skills/missing")
        self.assertFalse(ok)
        install_dir.assert_not_called()


class InstallSkillDirectoryTest(IsolatedHomeTest):
    def test_installs_valid_skill(self):
        skill = make_skill(self.src)
        with redirect_stdout(io.StringIO()):
            self.assertTrue(install_skill.install_skill_directory(skill))
        self.assertTrue((self.claude / "demo-skill" / "SKILL.md").exists())

    def test_rejects_unsafe_skill_name(self):
        skill = make_skill(self.src)
        with redirect_stdout(io.StringIO()):
            self.assertFalse(install_skill.install_skill_directory(skill, skill_name="../escape"))
        self.assertFalse((self.claude.parent / "escape").exists())

    def test_rejects_symlink_pointing_outside_skill(self):
        skill = make_skill(self.src)
        secret = Path(self.tmp.name) / "id_rsa"
        secret.write_text("PRIVATE KEY", encoding="utf-8")
        (skill / "notes.md").symlink_to(secret)
        with redirect_stdout(io.StringIO()):
            self.assertFalse(install_skill.install_skill_directory(skill))
        self.assertFalse((self.claude / "demo-skill").exists())

    def test_force_without_yes_in_non_interactive_mode_keeps_existing(self):
        skill = make_skill(self.src)
        with redirect_stdout(io.StringIO()):
            install_skill.install_skill_directory(skill)
        (self.claude / "demo-skill" / "marker.txt").write_text("original", encoding="utf-8")
        with mock.patch.object(sys.stdin, "isatty", return_value=False), redirect_stdout(io.StringIO()):
            self.assertFalse(install_skill.install_skill_directory(skill, force=True))
        self.assertTrue((self.claude / "demo-skill" / "marker.txt").exists())

    def test_force_with_yes_replaces_existing(self):
        skill = make_skill(self.src)
        with redirect_stdout(io.StringIO()):
            install_skill.install_skill_directory(skill)
        (self.claude / "demo-skill" / "marker.txt").write_text("original", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertTrue(install_skill.install_skill_directory(skill, force=True, assume_yes=True))
        self.assertFalse((self.claude / "demo-skill" / "marker.txt").exists())


if __name__ == "__main__":
    unittest.main()
