---
name: saas-business-model
description: Designs value-based SaaS monetization models, pricing tiers, feature gates, usage-based metering, unit economics (CAC, LTV, payback), and payment gateway integration architecture (Stripe, Mercado Pago, Lemon Squeezy). Triggered by /monetize, /pricing, /billing, or when designing SaaS revenue models.
---

# SaaS Business Model & Monetization Architecture

## Overview

Monetization cannot be an afterthought bolted onto a finished app. `saas-business-model` calculates and structures the commercial engine of your SaaS, aligning pricing with the value delivered to the customer while safeguarding your unit economics.

## Core Pillars

### 1. Value Metric Identification
- Determine what the customer is happy to pay for:
  - Per active seat / user?
  - Per processed item (e.g. CVs parsed, videos generated, invoices extracted)?
  - Per monthly active contact / data storage volume?

### 2. Tiered Packaging Matrix

| Tier | Target Persona | Price Point | Feature Gates & Limits |
| :--- | :--- | :--- | :--- |
| **Starter / Free** | Solo / Evaluator | $0 or $19/mo | Basic features, strict volume limit (e.g. 5 extractions/mo), community support. |
| **Pro / Growth** | SMB / Power User | $49 - $99/mo | Full feature set, 500 extractions/mo, priority processing, webhook access. |
| **Enterprise / Custom** | Scaleups & Teams | $299+ /mo | Custom volume, SSO (SAML), SLA, dedicated support, custom integrations. |

### 3. Unit Economics & Gross Margin Safeguards
- Calculate LLM inference / API costs per transaction.
- **Rule of Thumb**: Target > 80% Gross Margin. If an LLM call costs $0.05, the customer must pay at least $0.25 - $0.50 per call equivalent.
- Model CAC (Customer Acquisition Cost), LTV (Lifetime Value), and target < 12-month CAC payback.

### 4. Billing Architecture & Webhook Handlers
- **Stripe**: Subscriptions, Checkout Sessions, Customer Portal, Webhook idempotency (`invoice.payment_succeeded`, `customer.subscription.deleted`).
- **Mercado Pago**: Pix, Checkout Pro, Subscriptions, IPN webhook handling for Latin American markets.
- **Usage-based Metering**: Real-time event tracking in database/Redis with sync to Stripe Metered Billing.

## Output Format

Save the monetization architecture in `brain/<conversation-id>/saas_monetization_spec.md`.
