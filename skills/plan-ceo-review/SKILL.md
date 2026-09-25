---
name: plan-ceo-review
description: Evaluates product strategy, market opportunity, monetization leverage, unit economics, and ruthless scope prioritization from an executive CEO/Founder perspective. Use before approving implementation plans or architectural roadmaps.
---

# Plan CEO Review

## Overview

Engineering teams often over-optimize for architectural elegance while building features that have zero commercial leverage. The `plan-ceo-review` evaluates any proposed feature or technical plan from the viewpoint of a product-focused CEO.

It asks: *Does this move our core business metric (MRR, Retention, Activation)? Are we building too much? Can we achieve 80% of the impact with 20% of the engineering effort?*

## When to Use

- After `office-hours` or `interview-me`, before technical architecture starts.
- When reviewing a PRD, RFC, or high-level project plan.
- When deciding whether to build in-house vs. buy/integrate third-party APIs.
- When pricing, packaging, or product tiers need alignment.

## Review Pillars

### 1. High-Leverage Scope vs. Scope Creep
- Identify the **1 single killer feature** that delivers 90% of the value.
- Mark all secondary nice-to-haves as **V2 / Post-Launch**.
- Challenge: *Can we ship this in 3 days instead of 3 weeks?*

### 2. Monetization & Business Model Alignment
- How does this feature map to revenue?
  - New customer acquisition?
  - Expansion / Upsell (moving from Free to Pro/Enterprise)?
  - Churn reduction / Defensibility?
- What is the pricing metric? (Per seat, per API call, flat subscription, usage tier).

### 3. Moat & Defensibility
- What stops a competitor or OpenAI/Google from copying this in 3 months?
- Proprietary data aggregation, specialized workflows, integrations, network effects, or domain UX speed.

### 4. Build vs. Buy vs. Leverage
- Don't build auth, billing, vector DBs, or complex email delivery if mature APIs (Supabase, Stripe, Resend, Pinecone/pgvector) exist.

## Output Format

Save the CEO review in `brain/<conversation-id>/ceo_review.md`:

```markdown
# CEO & Product Review: [Initiative Name]

## 1. Strategic Verdict
- **Status**: [APPROVED / APPROVED WITH SCOPE REDUCTION / REJECTED]
- **Target Business KPI**: [e.g., +15% Free-to-Paid Conversion, -20% Onboarding Dropoff]

## 2. Ruthless Scope Cuts (The 80/20 Knife)
- **KEEP (Must-have MVP)**:
  - [Core Flow Item 1]
  - [Core Flow Item 2]
- **CUT (Move to Backlog / V2)**:
  - [Complex feature 1]
  - [Secondary dashboard 2]

## 3. Monetization & Packaging Tier
- **Tier Placement**: [Free / Pro ($29/mo) / Enterprise ($299/mo)]
- **Usage Gates & Metering**: [e.g., 50 extractions/mo for Free, Unlimited for Pro]

## 4. Next Step
- Pass approved scope to `plan-design-review` and `plan-eng-review`.
```
