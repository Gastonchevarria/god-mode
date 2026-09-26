---
name: ralph-loop
description: Executes autonomous task loops using disk state, backpressure, and isolated contexts based on the Ralph Loop methodology. Use when the user asks to run a Ralph loop, autonomous task loop, or implement features from specs autonomously.
---

# Ralph Loop: Autonomous AI Task Loops

You are now executing tasks using the **Ralph Loop** methodology. 
The core philosophy is: **state lives on disk, not in the model's context**. Each iteration focuses on a single task, writes results back to disk, validates against backpressure, and commits.

## Core Principles
1. **Disk as Shared State**: `IMPLEMENTATION_PLAN.md` persists between iterations and acts as the coordination mechanism.
2. **Backpressure Steers Quality**: Tests, builds, and lints reject bad work. You MUST fix issues before committing or moving to the next task.
3. **No Assumptions**: Search the codebase before implementing; don't assume functionality is missing.
4. **Complete Implementations**: No placeholders or stubs.

## Expected Project Structure
Expect to read or create the following files in the workspace:
- `PROMPT_plan.md` / `PROMPT_build.md`: Mode-specific instructions.
- `AGENTS.md`: Operational guide containing build and validation commands.
- `IMPLEMENTATION_PLAN.md`: The prioritized task list.
- `specs/`: Directory containing requirement specs.

---

## Operating Modes

### 1. PLANNING MODE (Gap Analysis)
When asked to run in Planning Mode:
1. Study `specs/*` to learn the application specifications.
2. Study existing `IMPLEMENTATION_PLAN.md` (if present).
3. Study the source code (`src/` or equivalent) to understand existing code and shared utilities.
4. Compare specs against code to perform a **gap analysis**.
5. Create or update `IMPLEMENTATION_PLAN.md` as a prioritized bullet-point list of tasks yet to be implemented. 
6. **CRITICAL**: Do NOT implement anything in this mode. Only plan.

### 2. BUILDING MODE (Implementation)
When asked to run in Building Mode (or when executing a `/goal`):
1. **Pick**: Choose the most important uncompleted item from `IMPLEMENTATION_PLAN.md`.
2. **Verify**: Before making changes, search the codebase (don't assume it's not implemented).
3. **Implement**: Write the code completely. No placeholders.
4. **Validate (Backpressure)**: Run the tests, typecheck, and linter (as specified in `AGENTS.md` or standard project scripts like `npm test`). 
   - If tests fail, fix the code. Do not proceed until tests pass.
   - If tests are missing for the new functionality, write them.
5. **Update State**: When everything passes, update `IMPLEMENTATION_PLAN.md` to mark the task as done.
6. **Commit**: If it's a git repository, stage all changes (`git add -A`) and commit with a descriptive message.
7. **Repeat**: Move to the next task or exit if the loop is complete.

## Running Unattended
To run this loop fully autonomously, the user should invoke the agent with the `/goal` command (e.g., `/goal execute the Ralph Loop in build mode`). During a goal, aggressively follow the Building Mode steps until the `IMPLEMENTATION_PLAN.md` is complete.
