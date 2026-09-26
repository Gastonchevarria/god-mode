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

### Removed
- `zero` (upstream has no license) and `changelog-video` (ships commercial fonts).
