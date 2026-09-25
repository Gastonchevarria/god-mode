---
name: autoplan
description: Orchestrates an end-to-end automated planning pipeline spanning CEO Review, Design Review, Engineering Review, and Atomic Task Breakdown in a single unified workflow. Triggered automatically or via /goal and /autoplan.
---

# Autoplan (Unified Product Planning Pipeline)

## Overview

`autoplan` executes a structured multi-role pipeline that turns an ambiguous request or new feature idea into a production-ready, peer-reviewed implementation plan without human handoffs between intermediate steps.

## Pipeline Flow

```text
[Input Idea / Request]
        ↓
1. CEO Review (`plan-ceo-review`) -> Validate business impact & cut scope
        ↓
2. Design Review (`plan-design-review`) -> Define UX/UI tokens, flow & state hierarchy
        ↓
3. Engineering Review (`plan-eng-review`) -> Stress-test architecture & failure modes
        ↓
4. Specification (`spec-driven-development`) -> Create formal functional specification
        ↓
5. Task Breakdown (`planning-and-task-breakdown`) -> Produce atomic, ordered implementation tasks
        ↓
[Unified implementation_plan.md]
```

## How to Execute

1. Read the user's objective and constraints.
2. In sequence, generate the evaluation for each role (CEO -> Design -> Eng).
3. Synthesize the results into the standard Antigravity `implementation_plan.md` artifact.
4. Set `RequestFeedback: true` on the final plan artifact for user authorization before implementation.
