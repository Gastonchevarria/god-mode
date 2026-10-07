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

## 2026-10-06 — design skills on Opus 5.5 in a forked context (v1.4.0)

With `model: claude-opus-5-5` and `context: fork` in the five design skills, routing still picks the same skills: the frontmatter changes where a skill runs, not how Claude chooses it.

| Run | Result | Misses |
| --- | --- | --- |
| 6 design cases, 2 runs each (first) | 9 / 12 | not inspected |
| Same cases, 2 runs each (second) | 11 / 12 | 1 run of `motion-design` loaded no skill |

The `motion-design` case is the noisy one already noted above: its misses load no skill rather than a wrong one.

## 2026-10-06 — design pack without Figma (v1.5.0)

`figma-to-code` was removed. The two `design-to-web` cases now point to a mockup saved in the project instead of a Figma link, and the `figma-to-code` case became a `ui-states-verification` case.

| Case | Runs | Result |
| --- | --- | --- |
| `design-to-web` (ES and EN, mockup path) | 4 | 4 / 4 |
| `ui-states-verification` | 2 | 2 / 2 |
| `motion-design` | 2 | 2 / 2 |
| `motion-direction` (2 cases) | 4 | 4 / 4 |

End to end with `claude -p --model claude-fable-5-1`: `/god` routed a "build the button from design/pay-button.png" request to `design-to-web` with the image path in its arguments; Fable 5.1 routed, Opus 5.5 built, and no Figma tool was called.

