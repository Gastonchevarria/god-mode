# Skill descriptions and the skill-listing budget — 2026-10-14

## The problem

Claude Code sends Claude a list of every installed skill with its description. The list gets a share of the context window: `skillListingBudgetFraction`, 1% by default, at 4 characters per token. That is about 40,000 characters on a 1M-context model and 8,000 on a 200k one. When the list is longer, Claude Code keeps the descriptions of the most-used skills and lists the rest by name only. Claude can invoke a name-only skill when something names it (as `/god` does), but it cannot pick it from the request.

In a Cowork session with all four god-mode plugins and Cowork's own skills, 31 of the 35 `god-mode-dev` skills (every one after `autoplan`, from `backend-architect` to `using-agent-skills`) and Anthropic's document skills appeared by name only.

## The change

| | v1.8.1 | v1.9.0 |
| --- | --- | --- |
| Description limit | 300 characters | 200 characters |
| Skill list, as Claude reads it (`- plugin:name: description`) | 32,650 characters | 24,077 characters |
| Per pack: growth / dev / core / design | 15,484 / 9,706 / 6,173 / 1,287 | 11,112 / 7,597 / 4,494 / 874 |

Each description keeps what the skill does, its strongest two or three trigger phrases and its "Not for X (use Y)" pointer. Skills without a trigger phrase got one.

`/skill-doctor` in an isolated HOME with all 111 v1.9.0 skills and nothing else: Fable 5.1 and Sonnet 5.5 list every description; Haiku 4.5 (200k context) still lists almost all of them by name only. On a 200k-context model, install only the packs you use.

## Routing on Fable 5.1

`scripts/eval_routing.py`, 38 requests, 1 run each, up to 4 turns before the first skill call.

| Pack | v1.8.1 | v1.9.0 |
| --- | --- | --- |
| core | 9 / 12 | 10 / 12 |
| design | 6 / 6 | 5 / 6 |
| dev | 6 / 10 | 9 / 10 |
| growth | 9 / 10 | 9 / 10 |
| Total | 30 / 38 | 33 / 38 |

- Gains: `thermos`, `backend-architect`, `ci-cd-and-automation`, `planning-and-task-breakdown`.
- The `design-to-web` miss did not repeat: 6 / 6 in a rerun of both design-to-web requests, 3 runs each.
- Every miss, before and after, was a run that loaded no skill within 4 turns (Fable 5.1 often looks around the project first). No run picked a wrong skill.

## Caveats

- 1 run per request; a single case can move by one run.
- The first version of this run scored 0 / 38 for both versions: the eval stopped at the first text, and Fable 5.1 says what it will do before acting. `eval_routing.py` now waits up to `--max-turns`.
