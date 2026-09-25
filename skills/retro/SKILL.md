---
name: retro
description: Conducts post-mortem analysis and retrospective evaluations after shipping a feature, sprint, or resolving an incident. Identifies bottlenecks, extracts reusable patterns, and feeds learnings into persistent agent memory.
---

# Retro (Retrospective & Continuous Self-Learning)

## Overview

High-velocity engineering teams improve by reflecting systematically on completed work. The `retro` skill inspects the execution delta between the original plan and what actually happened, cataloging mistakes to avoid and positive patterns to repeat.

## When to Use

- Immediately after completing a significant milestone, feature release, or incident fix.
- When something failed unexpectedly or took 3x longer than anticipated.
- Triggered by "retro", "post-mortem", "what did we learn?", or `/learn`.

## 4-Step Retrospective Process

1. **What Went Well?**:
   - Architectural decisions that saved time.
   - Clean abstractions or testing patterns that caught bugs early.
2. **What Went Wrong / Unexpected Friction?**:
   - Surprising dependency bugs, rate limits, unhandled edge cases, or broken assumptions.
3. **Root Cause Analysis (5 Whys)**:
   - Identify the foundational reason for any defect or delay.
4. **Actionable Upgrades (Feed into Memory)**:
   - Formulate new rules for `AGENTS.md` or update skill instructions using the `/learn` pattern.

## Output Format

Save the Retrospective in `brain/<conversation-id>/retro.md`:

```markdown
# Milestone Retrospective: [Feature/Release Name]

## 1. Executive Summary
- **Outcome**: [Shipped on time / Delayed / Re-scoped]
- **Key Metrics Achieved**: [e.g. 100% test pass rate, 0 critical lints, <100ms API response]

## 2. Key Learnings & Golden Patterns
- [Pattern 1 that accelerated development]
- [Anti-pattern to avoid in future sprints]

## 3. Persistent Knowledge Updates
- [Recommendation for AGENTS.md or local skills]
```
