# Routing eval — god-mode-design — 2026-10-05

Run with `python3 scripts/eval_routing.py --runs 2` on the 4 design cases in `tests/evals/routing.json`, loading god-mode-core and god-mode-design together.

| Expected skill | Correct | Other skill | No skill used |
| --- | --- | --- | --- |
| `design-to-web` (2 cases, ES and EN) | 4 / 4 | 0 | 0 |
| `figma-to-code` | 2 / 2 | 0 | 0 |
| `motion-design` | 2 / 2 | 0 | 0 |

- First run of the two `design-to-web` cases scored 0 / 4: the queries said "link del frame" without a URL, and Claude asked for the link instead of loading a skill (the limitation noted in `routing-2026-09-26.md`). With a Figma URL in the query, 4 / 4.
- Skill names and descriptions now total about 30,700 characters (111 skills), roughly 7,600 tokens.

## 2026-10-06 — adding motion-direction

Adding LottieFiles' skill as `motion-direction` lowered `motion-design` on "The modal feels stiff. Add spring-based animations…" from 5 / 6 runs (without it) to 5 / 12 (with it). Every miss was a run that loaded no skill, not the wrong one. The two descriptions were then split by job: `motion-design` writes animation code, `motion-direction` decides how motion should feel and points to `motion-design` for code.

| Case | Before the split | After the split |
| --- | --- | --- |
| `motion-design` (6 runs) | 3 / 6 | 5 / 6 |
| All 6 design cases (3 runs each) | — | 18 / 18 |
