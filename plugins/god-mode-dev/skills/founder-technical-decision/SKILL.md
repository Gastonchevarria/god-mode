---
name: founder-technical-decision
description: Documents high-impact architecture decision records (ADRs) with explicit categorization of reversibility (Type 1 one-way doors vs. Type 2 two-way doors), trade-offs, opportunity costs, and validation criteria. Triggered by /adr, /decision, or when evaluating critical technical choices.
---

# Founder Technical Decision (ADR Framework)

## Overview

Founders and lead engineers must make hundreds of technical choices under extreme uncertainty. Jeff Bezos famously categorized decisions into **Type 1 (One-Way Doors: irreversible, high stakes)** and **Type 2 (Two-Way Doors: easily reversible, low cost to pivot)**.

`founder-technical-decision` provides an executive Architecture Decision Record (ADR) format tailored for high-speed startup engineering.

## Decision Classification

- **Type 1 (One-Way Door)**: Primary Database engine (Postgres vs MongoDB vs DynamoDB), Core multi-tenant isolation model, Primary programming language/runtime.
  *Approach*: Require deep evaluation, stress-testing, and written alternatives.
- **Type 2 (Two-Way Door)**: UI component library, ORM vs raw SQL queries, email sending provider, specific charting library.
  *Approach*: Make the decision in under 15 minutes, pick the most familiar tool, move fast.

## Standard ADR Format

Save in `brain/<conversation-id>/architecture_decision_[topic].md`:

```markdown
# Architectural Decision Record: [Decision Title]

## 1. Context & Business Problem
- What problem are we solving?
- What are the operational and cost constraints?

## 2. Decision Classification
- **Type**: [Type 1: One-Way Door / Type 2: Two-Way Door]
- **Reversibility Score**: [High / Medium / Low]

## 3. Options Evaluated
| Option | Pros | Cons | Est. Cost / Complexity |
| :--- | :--- | :--- | :--- |
| **Option A (Chosen)** | [Key advantages] | [Acceptable trade-offs] | [Low/Medium] |
| **Option B** | [...] | [Why discarded] | [...] |
| **Option C** | [...] | [Why discarded] | [...] |

## 4. Rationale & Trade-offs Accepted
- Why Option A is optimal today.
- What friction we are intentionally accepting.

## 5. Validation & Trigger to Re-evaluate
- How do we know this decision was right?
- What event or scale (e.g. 100k DAU) would trigger a redesign?
```
