---
name: self-learning-skills
description: Captures golden path procedures, reusable workflows, setup steps, and troubleshooting patterns into persisted SKILL.md and AGENTS.md files for continuous agent self-improvement.
---

# Self-Learning Skills & Golden Path Persistence

This skill enables the agent to continuously learn, document, and persist "golden path" procedures discovered during development, debugging, backtesting, and deployment.

## When to Trigger This Skill

Activate this workflow whenever:
1. A complex multi-step task succeeds after trial, debugging, or troubleshooting.
2. A critical procedure (e.g. backtesting, strategy configuration, kill switch recovery, deployment) is established.
3. Repetitive setup instructions or environment configurations are clarified.

## Core Rules & Principles

1. **Capture Golden Paths**: Document the exact sequence of commands, directory structures, and configurations that resulted in verified success.
2. **Never Persist Plaintext Secret Keys**: Record environment variable names (e.g. `NVIDIA_API_KEY`, `BINANCE_API_KEY`) and secret managers instead of raw secrets.
3. **Structured Documentation**:
   - Save reusable procedures into `skills/<skill-name>/SKILL.md`.
   - Update project rules in `AGENTS.md`.
4. **Validation Required**: Only persist procedures that have been empirically executed and verified (e.g., green test output, clean build, verified HTTP status).

## Workflow Steps

### Step 1: Detect a Learned Workflow
When a procedure reaches a verified working state (e.g., successful API deployment, strategy tuning, backtesting run):
- Extract the prerequisite setup steps.
- Isolate the exact terminal commands and file paths.
- Document known failure modes and how to resolve them.

### Step 2: Structure as a Skill
Create or update `skills/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: <concise summary of when and how to use this skill>
---

# <Skill Title>

## Prerequisites
- List required environment variables, Node.js version, and system dependencies.

## Verified Command Workflow
1. Step 1: Command and expected output.
2. Step 2: Command and expected output.

## Troubleshooting & Failure Modes
- Issue: Description of error.
- Resolution: Step-by-step fix.
```

### Step 3: Register & Persist
Save the new skill to the workspace `.agents/skills/<skill-name>/SKILL.md` or global customization directory so future agent sessions inherit the learned knowledge automatically.
