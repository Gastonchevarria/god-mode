import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("eval_god", ROOT / "scripts" / "eval_god.py")
eval_god = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(eval_god)

KNOWN = {"TECH-ARCH", "SCOPE-KILLER", "DEBUGGING"}


class RunPassesTest(unittest.TestCase):
    def test_right_route_without_the_expected_skill_fails(self):
        case = {"route": "TECH-ARCH", "skills": ["plan-eng-review"]}
        run = {"route": "TECH-ARCH", "skills": []}
        self.assertFalse(eval_god.run_passes(case, run, KNOWN))

    def test_right_route_with_an_expected_skill_passes(self):
        case = {"route": "TECH-ARCH", "skills": ["plan-eng-review", "mvp-scope-killer"]}
        run = {"route": "TECH-ARCH", "skills": ["mvp-scope-killer"]}
        self.assertTrue(eval_god.run_passes(case, run, KNOWN))

    def test_case_without_skills_scores_the_route_only(self):
        case = {"route": "TECH-ARCH"}
        run = {"route": "TECH-ARCH", "skills": []}
        self.assertTrue(eval_god.run_passes(case, run, KNOWN))

    def test_wrong_route_fails_even_with_the_skill(self):
        case = {"route": "TECH-ARCH", "skills": ["plan-eng-review"]}
        run = {"route": "DEBUGGING", "skills": ["plan-eng-review"]}
        self.assertFalse(eval_god.run_passes(case, run, KNOWN))


if __name__ == "__main__":
    unittest.main()
