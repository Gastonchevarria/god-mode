# Changelog

All notable changes to god-mode are documented here. Versions follow [Semantic Versioning](https://semver.org/).

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
