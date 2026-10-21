# Changelog

All notable changes to god-mode are documented here. Versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `god-mode claude-via plugins`: for Claude Code, skills, hooks and subagents come from the god-mode plugins uploaded to the Claude app (which also load in the app's Claude Code sessions), so the CLI removes its own links, agent copies and hooks and keeps the protocol in `CLAUDE.md`, Antigravity and Cursor; `update` and `doctor` respect the mode; `claude-via installer` reverts it.
- Loop breaker: `plugins/god-mode-core/hooks/loop_breaker.py`, a PreToolUse hook on Bash that blocks the fourth run in a row of the same command (`GOD_MODE_LOOP_MAX`, `0` turns it off), installed by `god-mode doctor --fix` and loaded by the plugin; `god-mode doctor` checks it. The token rule now caps retries at 2 per step and asks for quiet test and linter output.
- Protocol §5 "Cambios quirúrgicos y simples" (`config/CLAUDE.md`, `protocol.md`, `.cursorrules`, Gemini rules): every changed line comes from the request, the minimum code that solves it, and the reading taken is named before starting. Adapted in our own words from the principles in [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) (MIT); the overlap with `code-simplification`, `incremental-implementation`, `spec-driven-development` and `test-driven-development` is why it is a rule, not a skill.
- `scripts/validate.py`: every route in the `/god` matrix must load a skill; only DIRECTA and CODE-MAP may load none. `tests/test_eval_god.py` covers the new scoring.
- `scripts/eval_god.py`: a case can list `skills`; it passes only when /god picks the route and loads one of them. New TECH-ARCH case: audit an existing system and propose an MVP.

### Fixed
- `/god` answered "Ruta: TECH-ARCH · Skills: ninguna" for an audit-and-MVP request. Rule 3 now says only DIRECTA, CODE-MAP and `god-mode usage` load no skill, and TECH-ARCH sends reviews of an existing system to `plan-eng-review`.

### Changed
- Protocol (§0–1 of `config/CLAUDE.md`, `.cursorrules`, `AGENTS.md`, Antigravity rules): one "sí" covers only the action shown, so an approved commit does not authorize the push. "Never Stop Short" now names when the agent stops: an Autonomy Limits action, a user who asked to see the plan or diff first, or a decision only the user can make. The role line is gone.
- Token rules: failed commands and tests are read in full; the 3-files-per-turn, 100-line and 2-skills-per-turn caps are gone; `/compact` is recommended by stale context, not by call counts.
- Subagents: no forced praise sections; no links to `docs/agents.md` or the missing performance checklist; "Invoke via" says they are launched from the main session (`/thermos` launches the two thermo agents), with the `god-mode-core:` prefix when god-mode loads as a plugin.

## [1.12.0] - 2026-10-15

### Added
- SessionStart hook `graphify_refresh.py`: when a session starts and after each compaction, in a project with `graphify-out/graph.json`, it runs `graphify update .` in the background (code only, local, no LLM). It prints nothing, so it adds no tokens. It finds the CLI on `PATH` or in `~/.local/bin`, where `uv tool` installs it and where the desktop app may not look. `GOD_MODE_GRAPHIFY_REFRESH=off` turns it off. Loaded by the god-mode-core plugin and written by `god-mode doctor --fix`, which also checks it.

### Changed
- Compaction goes back to when the context fills the `autoCompactWindow` of 200,000 tokens (about 187,000, after the 13,000 Claude Code keeps for the summary). `god-mode doctor --fix` no longer sets `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`, and removes the `70` that 1.11.0 wrote if it is still there.

## [1.11.0] - 2026-10-15

### Added
- `god-mode doctor --fix` sets `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70`: Claude Code compacts on its own at 70% of the auto-compact window, about 140,000 tokens with `autoCompactWindow` 200000. Without it, Claude Code compacts at the window minus 13,000 tokens. In three days of one user's Claude Code, the four sessions with a recorded cost reached 656,000 to 974,000 tokens of context and cost US$ 1,741 at API prices.
- `god-mode usage` shows each session's main model, hides empty sessions, counts the times the context was written again because the cache had expired (and says whether the cache lasts 5 minutes or 1 hour), and lists projects whose Graphify graph nobody queried.

### Changed
- The protocol block in `~/.claude/CLAUDE.md` went from 7,800 to 3,800 characters. The command table, the skill-install steps and the subagent list repeated what the skill and agent descriptions already say; `/install-skill` keeps the install steps.
- Token rule "Compactación": compaction at 70% is automatic in Claude Code; on a change of topic, Claude suggests `/clear` or a new session instead of compacting.
- README: Graphify's strict Read hook (`graphify hook-guard read --strict`). In one user's six repos, the soft hook had never led to a `graphify query`.

## [1.10.0] - 2026-10-14

### Added
- `god-mode usage [--days=N]` shows where Claude Code's tokens went: cost per session as Claude Code computes it, cache reads (subagents included), the largest context, compactions, subagents and skills, and `claude -p` sessions such as AutoHarness. It only reads `~/.claude/projects`.
- `god-mode doctor --fix` sets `autoCompactWindow` to 200000 when it is not set, and `doctor` reports it. With a 1M-token window, a Cowork session reached 783,000 tokens before compacting, and every model call re-read that context: 399 million cache-read tokens in one session.

### Changed
- The post-compact prompt audit covers only the instruction files that changed, runs in a Sonnet subagent with the session's model as the target, and leaves out skills linked into `~/.claude/skills` (god-mode's own). It used to audit the whole working directory on the session's model: about 2.6 MB of Markdown in the god-mode repo, and every god-mode update triggered it in every project. Above 60 KB of changed files Claude only offers the audit (`GOD_MODE_PROMPT_AUDIT_MAX_KB`). The first run after updating takes today's files as the baseline instead of auditing everything.
- CODE-MAP in `/god` uses the Graphify CLI and no longer loads the project's `graphify` skill, which is about 43 KB and meant for building graphs with `/graphify`. The README explains how to stop Claude from loading that skill on its own.
- CONTEXT-HEALTH: pass the files to audit to `prompt-audit`, and `god-mode usage` for "where did my tokens go".

## [1.9.0] - 2026-10-14

### Changed
- Every skill description is 200 characters or fewer, down from 300, and `scripts/validate.py` enforces it. The skill list Claude reads went from about 32,700 to 24,100 characters. Claude Code gives that list 1% of the context window and lists the skills that do not fit by name only; in Cowork, with all four packs and Cowork's own skills, 31 of the 35 `god-mode-dev` skills had lost their descriptions.
- Skills that had no trigger phrase (`backend-architect`, `agent-mcp-builder`, `ai-product-eval-ops`, `fastapi-pro`, `nextjs-app-router`, `rag-implementation`, `retro`, `self-learning-skills` and others) now say when to use them. `shipping-and-launch` (deploys) and `launch` (marketing) point to each other.

### Fixed
- `scripts/eval_routing.py` gives the model up to four turns (`--max-turns`) before its first skill call. It used to stop at the first text, so a model that says what it will do before acting (Fable 5.1) scored as "no skill". API errors such as spend limits now count as failed runs instead of "no skill".

On Fable 5.1 (38 requests, 1 run each), routing went from 30/38 to 33/38; `god-mode-dev` from 6/10 to 9/10. No run picked a wrong skill, before or after. Details in `docs/evals/skill-listing-2026-10-14.md`.

## [1.8.1] - 2026-10-13

### Fixed
- CODE-MAP and the README now add `graphify cluster-only . --no-label` after `graphify extract . --code-only`. `extract` writes only `graph.json`; the report and `graph.html` come from `cluster-only`, and `--no-label` keeps community naming off any LLM API.

## [1.8.0] - 2026-10-13

### Added
- CODE-MAP route in `/god` for questions about how the code connects: what depends on a module, what breaks if a signature changes, the call path between two points. When the project has a [Graphify](https://github.com/Graphify-Labs/graphify) graph (`graphify-out/graph.json`), Claude asks it first with `graphify query`, `path`, `explain` or `affected`, and reads files only for what the graph does not answer. Without a graph it builds one with `graphify extract . --code-only` (local AST, no API); without the CLI it searches as before and says how to install it.
- Token rule: with `graphify-out/graph.json` in the project, query the graph before a broad grep.
- `god-mode doctor` reports whether the Graphify CLI is installed. It is optional, so a missing CLI does not fail the check.
- `scripts/validate.py` accepts `graphify` as a skill installed by its own CLI.
- Two CODE-MAP requests in `tests/evals/god_routes.json`.

## [1.7.0] - 2026-10-10

### Added
- Prompt audit after compacting. A SessionStart hook (matcher `compact`) checks whether the instructions that load in the project changed since the last audit: CLAUDE.md, CLAUDE.local.md and AGENTS.md in the project, its parents and subfolders, and the rules, skills, commands, subagents and output styles under `.claude/` and `~/.claude/`. It compares sizes and modification times, not contents. When they changed, Claude runs Claude Code's `/claude-api prompt-audit` in a subagent on the session's model, shows the findings and edits nothing without the user's "yes". `GOD_MODE_PROMPT_AUDIT` takes `changed` (default), `always` or `off`.
- The hook ships in the god-mode-core plugin, and `god-mode doctor --fix` writes it into `~/.claude/settings.json`; `god-mode doctor` checks it.
- `/god` CONTEXT-HEALTH route: "audit my CLAUDE.md and skills" runs prompt-audit in a subagent. `scripts/validate.py` accepts skills that ship with Claude Code (`claude-api`) in the route matrix.

### Fixed
- Issues the first audit found in the global protocol (`config/CLAUDE.md`): it told Claude to "always leverage" five skills, against `/god`'s one-skill rule; `/security` pointed to a `claude-security` skill that does not exist instead of `security`; and the skill installer was described as "autonomous", although it asks for confirmation.

## [1.6.0] - 2026-10-06

### Added
- A DIRECTA route in `/god`: small changes, questions, explaining code, commands and commit messages are done directly, without loading a skill.
- `scripts/eval_god.py` and `tests/evals/god_routes.json`: 22 requests that check which route `/god` picks, which skills it loads, whether it re-reads the protocol and what the first turns cost. Results in `docs/evals/god-routes-2026-10-06.md`.

### Changed
- Every `/god` route loads one skill, the one that fits the request; another skill joins only when a later step needs it. Billing code (`saas-launch-revenue`) moved from GROWTH to MONETIZATION, and FULL-BUILD starts with `incremental-implementation`, or `autoplan` for a big or unclear feature.
- `/god` no longer re-reads `references/protocol.md`: the session already carries the protocol through `CLAUDE.md`, the Antigravity rules or the plugin hook. It reads the file only when the protocol is missing.
- The `⚡ GOD` line comes before any tool call, including loading a skill.
- `/god` with no request lists what it can do and asks what you need.
- `scripts/validate.py` checks every skill named in the route matrix, not only lines that say "Activa".

On the route eval (Opus 5.5, 44 runs): right route 43 → 44, runs that loaded two skills 5 → 0, protocol re-reads 26 → 0.

## [1.5.0] - 2026-10-06

### Removed
- `figma-to-code` and every use of the Figma MCP server in the design pack. Design work no longer depends on Figma reads or on a `.figma-cache/` folder; projects that have one can delete it.

### Changed
- `design-to-web` builds from a reference image saved in the project (passed by its path), the project's design system or a description. Values read off an image are marked `≈` and mapped to the closest existing token.
- The `/god` DESIGN route activates only the skill the request needs: `design-to-web` to build, `motion-direction` to decide how motion feels, `motion-design` for animation code, `ui-states-verification` to check states in the browser.
- `ui-states-verification` compares against the reference image when there is one, and skips the fidelity check otherwise.

## [1.4.0] - 2026-10-06

### Changed
- The five god-mode-design skills run on `claude-opus-5-5` in a forked context (`model` and `context: fork` in their frontmatter). The main session keeps the model chosen in the interface: with Fable 5.1 as the default, `/god` routes on Fable 5.1, the design work runs on Opus 5.5 and its subagents on Sonnet 5.5. Checked with `claude -p`: a `/god` design request used Fable 5.1 for routing and Opus 5.5 for the build; the next turn went back to Fable 5.1. Without `context: fork`, `model` applies only when the user types the skill's command, not when Claude or `/god` picks the skill.
- `design-to-web` states that a forked skill does not see the conversation, so it returns a question when its arguments lack something essential.

### Fixed
- `figma-to-code` saves `.figma-cache/` even when it cannot write `.git/info/exclude`, and asks the user to add the folder to `.gitignore`. Before, a denied write skipped the cache, and the next run spent another Figma read.

## [1.3.1] - 2026-10-06

### Fixed
- The design module's command is `/design-to-web`. `/design` is a built-in Claude Code command (access to Claude Design projects), so typing it never reached the skill. The global protocol table and the `design-to-web` description now say `/design-to-web`.

## [1.3.0] - 2026-10-06

### Added
- `motion-direction` in god-mode-design: LottieFiles' motion-design skill (MIT, [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill) at `f9a8a04`), renamed so it does not clash with god-mode's `motion-design`. It decides what motion should feel like: four personalities with their durations and easing, duration tables per element, stagger budgets, emotion-to-motion mapping and Disney's 12 principles for UI, with 16 reference files. A note under its title sets precedence: on UI controls the ambient layer is optional, loops over 5 seconds need a pause control, and `motion-design` wins on animated properties and reduced motion.
- `motion-design` starts from `motion-direction`'s personality and maps it to springs. The DESIGN route and `design-to-web` include it. The suite now has 112 skills.
- Two `motion-direction` cases in the routing eval.
- The `motion-design` and `motion-direction` descriptions split the work: one writes animation code, the other decides how motion should feel. Without the split, adding `motion-direction` made Claude skip `motion-design` more often (`docs/evals/routing-design-2026-10-05.md`).

### Fixed
- Generated credits say "1 skill" instead of "1 skills".

## [1.2.1] - 2026-10-06

### Changed
- `figma-to-code` spends one Figma MCP read per component, two at most, instead of four. `get_design_context` already returns the reference code, the screenshot and the asset URLs; `get_variable_defs` runs only when that code uses raw values. A link without `node-id` is answered with a question instead of a `get_metadata` read. On Figma's Starter plan (20 reads per month) that is about 10 to 20 components per month instead of 5.
- Responses are cached in `.figma-cache/` (kept out of git through `.git/info/exclude`) and reused until the design changes; `ui-states-verification` compares against the cached screenshot. Every run reports the reads it used, and a rate-limit error stops the run instead of retrying.

## [1.2.0] - 2026-10-05

### Added
- `god-mode-design` plugin (pack `design`) with four skills: `design-to-web` (the conductor, `/design`), `figma-to-code` (exact tokens, variables, layers and a reference screenshot through the Figma MCP server; never guessed from a screenshot), `motion-design` (spring transitions, press feedback, staggered entrances, smooth skeletons, `prefers-reduced-motion` fallback, `transform` and `opacity` only) and `ui-states-verification` (Playwright drives hover, focus-visible, active, disabled, loading and error, compares each state against Figma, checks 44 px touch targets, reduced motion and a11y).
- DESIGN route in `/god` and a `/design` row in the global protocol table. The suite now has 111 skills.
- Four design cases in the routing eval.

## [1.1.1] - 2026-09-30

### Changed
- The recommended subagent model is now `claude-sonnet-5-5`. Run `god-mode doctor --fix` to update `~/.claude/settings.json`.

### Fixed
- `god-mode doctor` reads `CLAUDE_CODE_SUBAGENT_MODEL` and the other variables from `~/.claude/settings.json` before the shell's environment, the same order Claude Code applies them.

## [1.1.0] - 2026-09-27

### Added
- `config/rules/token-optimization.md`: global rule for brevity, context hygiene, tool-call discipline, output frugality, compaction triggers and skill loading. `install.sh` adds it to the managed block in `~/.claude/CLAUDE.md` and to Antigravity's rules.
- `auto-compact` skill in god-mode-core: rates session health 🟢🟡🔴 and compacts with a structured summary after the user agrees.
- CONTEXT-HEALTH route in `/god` (`auto-compact` + `context-engineering`).
- `god-mode doctor`: read-only check of the installation and the recommended settings, with the exact fix for each failure.
- README section on token optimization and the recommended `CLAUDE_CODE_SUBAGENT_MODEL`, output style and optional AutoHarness settings.
- The god-mode-core plugin loads the protocol and the global rules when a session starts (a `SessionStart` hook), so the plugins alone, in Claude Code or in the Claude app, enforce the autonomy limits and the token rules. The hook stays silent when `~/.claude/CLAUDE.md` already has the installer's block, so the protocol never loads twice.
- `god-mode doctor --fix` writes the recommended output style and variables into `~/.claude/settings.json`, with a backup, keeping every other key.
- `god-mode doctor` reads the variables from `~/.claude/settings.json` too, and warns when god-mode is loaded twice in Claude Code (plugins plus the installer's links).

### Changed
- `context-engineering` moved from god-mode-dev to god-mode-core. The suite now has 107 skills.

## [1.0.1] - 2026-09-26

Upgrading from a version before 1.0.0 now works: run the installer once more.

### Security
- Closed the six CodeQL alerts in the vendored archify skill: tag and `<iframe>` stripping repeats until nothing changes, a test fixture server no longer echoes request text into HTML, and two no-op replacements are gone.

### Fixed
- The installer upgrades pre-1.0 installs. It replaces the old links into `~/.gemini/config/plugins`, and lists the real folders with a god-mode skill's name and the old Antigravity plugin folders it won't touch, instead of silently keeping them. On a real pre-1.0 install, 1.0.0 linked 0 of 106 skills in Claude Code; 1.0.1 links 99.
- CI passes on `main`: ruff is pinned to 0.16.9 with its findings fixed, and the smoke tests pass on release commits and on macOS.
- `tests/smoke.sh` no longer rewrites the developer's `origin` remote.
- archify: brand marks regenerated for simple-icons 16.32.0.
- archify: four update-notifier tests that hold a network request open no longer time out on loaded CI runners (they used the 50 ms test default).

### Added
- CI runs archify's own test suite with `scripts/test_archify.py`, excluding only the tests that read files from the upstream archify repository (listed in `config/archify-tests.json`).
- `AGENTS.md` tells agents such as Antigravity how to install god-mode: run the installer, never copy plugins by hand.

### Changed
- README rewritten: 30-second install, what `/god` routes to, the protocol in plain words, and an FAQ.
- GitHub Actions `actions/checkout` and `actions/setup-python` v7; archify dev dependencies parse5 8.0.1 and simple-icons 16.32.0.

## [1.0.0] - 2026-09-26

First release. Skills moved to a plugin marketplace (see README). If you installed with `install.sh` before this version, run it once more.

### Security
- `scripts/install-skill.py` no longer runs git through a shell. A crafted URL could execute arbitrary commands.
- The installer validates every URL component, rejects `..` and dot segments, refuses symlinks that point outside a skill, and asks before overwriting or before installing several skills from one repository.
- The protocol (`CLAUDE.md`, `god`, `GEMINI_RULES.md`, `.cursorrules`, `AGENTS.md`) now requires explicit approval before push, deploy, deletes, database migrations, money or credentials, messages to third parties and external installs.

### Fixed
- Switching packs now cleans Antigravity too, and broken links no longer crash it.
- `god-mode update` reports git failures and exits non-zero instead of claiming success.
- `install.sh` detects tools before creating their folders and no longer writes `.cursorrules` or `AGENTS.md` into the current folder unless `--cursor` is passed.
- Existing `~/.claude/CLAUDE.md` files now receive protocol updates through a managed block. Older installs are migrated, keeping the user's own rules and a backup.
- `god-mode update` now also updates the CLI itself, and an outdated copy in `/usr/local/bin` is updated or reported.
- Backups never overwrite each other, and `curl | bash` no longer mistakes the current folder for the repository.

### Added
- `install.sh --version=vX.Y.Z` installs a published release. Releases include `install.sh.sha256`.
- CI on every pull request: `scripts/validate.py`, unit tests, end-to-end install tests on Linux and macOS, ruff and shellcheck.
- `THIRD_PARTY.md` and `licenses/` credit the upstream projects.
- Claude Code plugin marketplace with three plugins: god-mode-core, god-mode-dev and god-mode-growth.
- `scripts/eval_routing.py` and `tests/evals/routing.json` measure whether Claude picks the right skill. Results in `docs/evals/`.

### Changed
- Every skill description is now 300 characters or fewer, with concrete trigger phrases and a boundary against its closest sibling. Descriptions went from about 16,400 to 7,300 tokens, and CI enforces the limit.
- Seven SKILL.md files over 3,000 words were split: long reference material moved verbatim into `references/`, with pointers saying when to read it.
- The /god banner is one line instead of four.
- The five rendered HTML examples of `archify` (3.5 MB) moved to `docs/archify-examples/` so they are not installed with the plugin.

### Removed
- `zero` (upstream has no license) and `changelog-video` (ships commercial fonts).
- The whole video toolkit (HyperFrames, captions, motion graphics, video production), 25 skills, plus the growth `video` skill, to keep the suite focused on engineering and growth.
- `startup-god-router`, a duplicate of `god`.
