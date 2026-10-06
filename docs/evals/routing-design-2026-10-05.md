# Routing eval — god-mode-design — 2026-10-05

Run with `python3 scripts/eval_routing.py --runs 2` on the 4 design cases in `tests/evals/routing.json`, loading god-mode-core and god-mode-design together.

| Expected skill | Correct | Other skill | No skill used |
| --- | --- | --- | --- |
| `design-to-web` (2 cases, ES and EN) | 4 / 4 | 0 | 0 |
| `figma-to-code` | 2 / 2 | 0 | 0 |
| `motion-design` | 2 / 2 | 0 | 0 |

- First run of the two `design-to-web` cases scored 0 / 4: the queries said "link del frame" without a URL, and Claude asked for the link instead of loading a skill (the limitation noted in `routing-2026-09-26.md`). With a Figma URL in the query, 4 / 4.
- Skill names and descriptions now total about 30,700 characters (111 skills), roughly 7,600 tokens.
