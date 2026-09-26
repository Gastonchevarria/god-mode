---
name: plan-eng-review
description: Evaluates system architecture, failure modes, data modeling, concurrency, rate limits, testing strategy, error handling, and API contract boundaries from a Principal/Staff Engineer perspective.
---

# Plan Engineering Review

## Overview

A robust product requires rock-solid engineering foundations. `plan-eng-review` stress-tests technical designs before code is written, uncovering hidden edge cases, race conditions, N+1 queries, unhandled external API failures, and missing error boundaries.

## When to Use

- After CEO and Design reviews, before drafting atomic tasks or implementation.
- When designing database schemas, backend services, or complex API endpoints.
- When integrating with external AI APIs, payment webhooks, or third-party OAuth.

## Principal Engineer Review Checklist

### 1. Data Integrity & Schema Design
- Proper normalization vs. deliberate denormalization.
- Foreign keys, cascading behaviors, indexing on query filters/sorts.
- Idempotency keys on mutations and financial transactions.

### 2. Failure Modes & Resilience
- What happens when OpenAI / Anthropic / Stripe returns 503 or 429?
- Backoff, retry policies, exponential jitter, circuit breakers, fallback models.
- Graceful degradation in the UI when background jobs are queued or delayed.

### 3. Concurrency & Rate Limiting
- Race condition mitigation (e.g., atomic DB updates, Redis locks).
- API token bucket / leaky bucket per IP/User.

### 4. Testing & Verification Pyramid
- Unit tests for pure business logic & parsers.
- Integration tests for database queries and webhook processors.
- End-to-end sanity tests for critical user conversion paths.

## Output Format

Save the Engineering review in `brain/<conversation-id>/eng_review.md`:

```markdown
# Engineering Review: [Architecture/Feature Name]

## 1. Architectural Architecture Summary
- **Data Flow**: Client -> [API/Edge] -> [Service Layer] -> [DB / Vector Store / Cache]
- **Key Abstractions**: [Services, Repositories, MCP Tools]

## 2. Risk Matrix & Mitigations
| Failure Mode | Likelihood | Impact | Mitigation Strategy |
| :--- | :---: | :---: | :--- |
| External API 429/500 | Medium | High | Exponential backoff + fallback model |
| Double Webhook Delivery | High | Critical | Idempotency table check |
| Slow Vector Search Query | Medium | Medium | HNSW index + Redis query cache |

## 3. Testing & Verification Gates
- [Unit test suite paths]
- [Integration test plan]

## 4. Engineering Verdict
- [PASSED TO SPEC-DRIVEN IMPLEMENTATION / REQUIRES SCHEMA REVISION]
```
