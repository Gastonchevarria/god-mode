# Prompt audit after compacting — 2026-10-10

Test of the SessionStart hook (`plugins/god-mode-core/hooks/prompt_audit_check.py`) with `claude -p`, Opus 5.5, in an isolated HOME with god-mode installed (pack `all`, 111 skills) and a project with its own `CLAUDE.md`. The hook found 119 instruction files.

Claude Code's bundled `claude-api` skill is turned off in the test environment by a managed `skillOverrides` policy, the same one Cowork uses. The runs that needed it loaded a local copy of Anthropic's public `claude-api` skill as a plugin (`apitest:claude-api`).

| Step | Result |
| --- | --- |
| `/compact` | The hook ran (`SessionStart:compact`) and added its context; a second compaction of the same session with no file changes added nothing |
| Next turn, `claude-api` turned off | One line saying the skill is not available, then on with the conversation |
| Next turn, `claude-api` available, reads allowed | The main session launched one subagent with `model: "opus"`; it loaded the skill with the argument `prompt-audit`, ran 22 shell commands and 1 read, and edited nothing. 26 findings (6 high confidence). The main session showed the top ones and offered the diff without applying it |
| Cost of that turn | US$ 2.39, almost all in the subagent; the main conversation peaked at 46,731 tokens |
| Next turn, reads not allowed (`claude -p` with no approver) | The subagent audited only what it could read, and the report said so on its first line |

Unit tests: `tests/test_prompt_audit_check.py` (first run, no change, nested and global changes, ignored folders, a second hook for the same compaction, `always`, `off`, non-compact sources, unknown model).

In an interactive session, Claude Code may ask before the subagent reads files outside the project, such as `~/.claude/skills`; that path was not tested here.
