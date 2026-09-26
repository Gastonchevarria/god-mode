import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("validate", ROOT / "scripts" / "validate.py")
validate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate)


class FakeRepo:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "config").mkdir()
        (self.root / "agents").mkdir()
        self.packs({"core": []})
        (self.root / "THIRD_PARTY.md").write_text("", encoding="utf-8")

    def skill(self, dirname, frontmatter):
        d = self.root / "skills" / dirname
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n# Body\n", encoding="utf-8")

    def packs(self, packs):
        (self.root / "config" / "packs.json").write_text(json.dumps({"packs": packs}), encoding="utf-8")

    def credit(self, *names):
        (self.root / "THIRD_PARTY.md").write_text(" ".join(f"`{n}`" for n in names), encoding="utf-8")

    def errors(self, max_description=300):
        errors = []
        with mock.patch.object(validate, "ROOT", self.root):
            skills = validate.check_skills(max_description, errors)
            agents = validate.check_agents(errors)
            validate.check_packs(skills, errors)
            validate.check_router(skills, agents, errors)
            validate.check_third_party(skills, errors)
            validate.check_plugins(errors)
        return errors


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.repo = FakeRepo()
        self.addCleanup(self.repo.tmp.cleanup)

    def test_valid_repo_has_no_errors(self):
        self.repo.skill("demo", "name: demo\ndescription: Does a thing.")
        self.repo.credit("demo")
        self.repo.packs({"core": ["demo"], "all": "ALL"})
        self.assertEqual(self.repo.errors(), [])

    def test_name_mismatch(self):
        self.repo.skill("demo", "name: other\ndescription: x")
        self.repo.credit("demo")
        self.assertTrue(any("does not match directory" in e for e in self.repo.errors()))

    def test_angle_brackets_and_length(self):
        self.repo.skill("demo", f"name: demo\ndescription: 'use <thing> {'a' * 400}'")
        self.repo.credit("demo")
        errors = self.repo.errors()
        self.assertTrue(any("'<' or '>'" in e for e in errors))
        self.assertTrue(any("characters (limit 300)" in e for e in errors))

    def test_manual_only_skill_is_flagged(self):
        self.repo.skill("demo", "name: demo\ndescription: x\ndisable-model-invocation: true")
        self.repo.credit("demo")
        self.assertTrue(any("disable-model-invocation" in e for e in self.repo.errors()))

    def test_unknown_pack_entry(self):
        self.repo.skill("demo", "name: demo\ndescription: x")
        self.repo.credit("demo")
        self.repo.packs({"core": ["demo", "ghost"]})
        self.assertTrue(any("unknown skill 'ghost'" in e for e in self.repo.errors()))

    def test_router_to_unknown_skill(self):
        self.repo.skill("god", "name: god\ndescription: router")
        (self.repo.root / "skills" / "god" / "SKILL.md").write_text(
            "---\nname: god\ndescription: router\n---\n- Ruta: X ➔ Activa `missing-skill`\n", encoding="utf-8")
        self.repo.credit("god")
        self.assertTrue(any("routes to unknown skill or agent 'missing-skill'" in e for e in self.repo.errors()))

    def test_skill_missing_from_third_party(self):
        self.repo.skill("demo", "name: demo\ndescription: x")
        self.assertTrue(any("not listed" in e for e in self.repo.errors()))

    def test_plugin_name_must_match_directory(self):
        manifest = self.repo.root / "plugins" / "core" / ".claude-plugin" / "plugin.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"name": "other"}), encoding="utf-8")
        self.assertTrue(any("does not match directory" in e for e in self.repo.errors()))


if __name__ == "__main__":
    unittest.main()
