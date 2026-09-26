---
name: autoplan
description: "Runs the full planning chain in one pass: CEO, design and eng reviews, then spec and task breakdown, merged into one implementation_plan.md. Use when asked to \"plan this end to end\", \"full plan for this feature\", /autoplan or /goal. For one lens, use that plan-*-review."
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
