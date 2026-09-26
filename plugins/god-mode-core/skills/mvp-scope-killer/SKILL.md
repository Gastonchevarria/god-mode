---
name: mvp-scope-killer
description: "Cuts premature over-engineering from an MVP plan (microservices, custom RBAC, in-house dashboards, hand-rolled auth, speculative abstractions) into a lean core. Use when the user says /scope-kill, 'cut scope', 'is this overkill for an MVP' or 'what can we drop'."
---

# MVP Scope Killer

## Overview

The death of startups is rarely a lack of features; it is almost always building too much before validating the core transaction. `mvp-scope-killer` acts as an aggressive scope editor, eliminating 50% to 80% of unnecessary complexity from initial roadmaps.

## The Scope Guillotine (What to Kill Immediately)

When reviewing any plan or feature list, actively detect and kill:

1. **Premature Microservices & Distributed Infrastructure**:
   - *Kill*: Splitting a new MVP into 5 microservices, Kafka queues, and Kubernetes.
   - *Replace With*: Clean modular monolith on Next.js/FastAPI + PostgreSQL.
2. **Elaborate Role-Based Access Control (RBAC)**:
   - *Kill*: Building granular 7-level permission matrices for an app with 0 users.
   - *Replace With*: Single `admin` vs `member` boolean flag.
3. **Vanity Analytics Dashboards**:
   - *Kill*: Custom BI charts and analytics suites that the founder wants to build in-house.
   - *Replace With*: Embedded PostHog / Mixpanel snippet or simple raw query table.
4. **Complex Custom Authentication**:
   - *Kill*: Hand-rolling OAuth, SMS 2FA, and password reset tokens from scratch.
   - *Replace With*: Supabase Auth, Clerk, NextAuth, or Firebase Auth.
5. **Speculative Abstractions & Generic Frameworks**:
   - *Kill*: Designing a generic multi-tenant plugin system before building the first plugin.
   - *Replace With*: Direct, straightforward code. Refactor only upon the 3rd concrete use case (Rule of Three).

## Scope Killer Report

Produce `brain/<conversation-id>/mvp_scope_pruning.md`:

```markdown
# MVP Scope Killer Report

## Original Scope Breakdown
- [Feature 1]
- [Feature 2]
...

## ✂️ Pruned Items (Moved to Post-PMF Backlog)
- **Killed**: [Complex Item 1] -> **Reason**: [Premature complexity]
- **Killed**: [Complex Item 2] -> **Reason**: [No direct impact on initial conversion]

## ⚡ Remaining Lean MVP Core (Shippable in < 48-72h)
1. [Atomic Flow Step 1]
2. [Atomic Flow Step 2]
3. [Atomic Flow Step 3]
```
