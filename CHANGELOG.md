# Changelog

All notable changes to god-mode are documented here. Versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Security
- `scripts/install-skill.py` no longer runs git through a shell. A crafted URL could execute arbitrary commands.
- The installer validates every URL component, rejects `..` and dot segments, refuses symlinks that point outside a skill, and asks before overwriting or before installing several skills from one repository.
- The protocol (`CLAUDE.md`, `god`, `GEMINI_RULES.md`, `.cursorrules`, `AGENTS.md`) now requires explicit approval before push, deploy, deletes, database migrations, money or credentials, messages to third parties and external installs.

### Fixed
- Switching packs now cleans Antigravity too, and broken links no longer crash it.
- `god-mode update` reports git failures and exits non-zero instead of claiming success.
- `install.sh` detects tools before creating their folders and no longer writes `.cursorrules` or `AGENTS.md` into the current folder unless `--cursor` is passed.
- Existing `~/.claude/CLAUDE.md` files now receive protocol updates through a managed block. Older installs are migrated, keeping the user's own rules and a backup.

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
