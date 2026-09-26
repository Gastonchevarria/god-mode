---
name: office-hours
description: "YC-style test of whether a raw idea is worth building: narrow ICP, hair-on-fire problem, why now, value metric, 48-hour smoke test; verdict proceed, pivot or kill. Use when asked \"is this worth building?\", \"validate this idea\", \"who is the customer?\" or \"office hours\"."
---

# Office Hours (YC / Founder Discovery)

## Overview

Most startup failures and wasted engineering sprints stem from building things nobody actually wants or building the wrong solution for an imaginary problem. 

`office-hours` acts as your Y Combinator-style sparring partner. It interrogates the hypothesis, strips away non-essential noise, and forces radical clarity on the target user (ICP), the painful problem being solved, and the fastest path to validated learning.

## When to Use

- When proposing a brand-new startup, product, or feature concept.
- When you have a "cool tech idea" but haven't validated the buyer or end-user pain.
- When pivoting or expanding into a new market segment.
- Before committing engineering resources to a multi-week roadmap.
- Triggered by `/grill-me`, "office hours", "validate this idea", "is this worth building?".

## The 5 Core Questions

In every office-hours session, you must rigorously answer and document:

1. **Who is the specific user? (Narrow ICP)**
   - Not "everyone" or "businesses", but "Solo founders running B2B SaaS under $10k MRR" or "Junior recruiters at 50-200 person tech companies".
2. **What is the urgent hair-on-fire problem?**
   - What painful, expensive, or tedious task are they doing right now?
   - How are they solving it today? (Spreadsheets, manual labor, clunky legacy software).
3. **Why now?**
   - What changed in the world (LLM capability, regulatory shift, new API, platform shift) that makes this solution possible/urgent today?
4. **What is the atomic value metric?**
   - What single metric proves the user received value in their first 5 minutes? (e.g., "Extracted 100 leads", "Generated custom proposal in 30s", "Automated a 2-hour invoice reconciliation").
5. **What is the simplest smoke test / validation experiment?**
   - What can be built in 48 hours to get a user to commit time, data, or money?

## Output Structure

Generate a structured report (e.g. in `brain/<conversation-id>/office_hours_discovery.md`):

```markdown
# Office Hours Discovery: [Product/Feature Name]

## 1. Problem & Customer ICP
- **Target User**: [Precise persona]
- **Hair-on-Fire Pain**: [Specific daily/weekly friction]
- **Current Workarounds**: [How they cope today]

## 2. Market Timing & Value Proposition
- **Why Now Catalyst**: [Enabling technology or market change]
- **The 10x Differentiator**: [Why this is 10x better, faster, or cheaper]
- **Atomic Value Moment (Aha! Moment)**: [Time-to-value milestone]

## 3. Top 3 Fatal Risks & Validation Tests
- **Risk 1**: [Assumption] -> **Test**: [Smoke test / Interview / Landing page test]
- **Risk 2**: [Assumption] -> **Test**: [...]
- **Risk 3**: [Assumption] -> **Test**: [...]

## 4. Verdict & Recommendation
- [PROCEED TO CEO REVIEW / PIVOT / NARROW SCOPE / KILL]
```

## Guardrails & Anti-Rationalization

- **Reject "AI for X" without workflow integration**: AI alone is not a moat; the workflow, data moat, and UX are.
- **Reject vague TAMs**: Don't accept "it's a $50B market". Focus on the initial $1M beachhead.
- **Enforce ruthless narrowing**: If the ICP has more than two personas, force the user to pick one.
