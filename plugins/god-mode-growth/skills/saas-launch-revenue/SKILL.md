---
name: saas-launch-revenue
description: Implements SaaS go-to-market revenue systems, pricing checkout flows, Stripe billing webhooks, dunning management, trial-to-paid conversion, and churn prevention mechanisms.
---

# SaaS Launch & Revenue Engine

## Overview

Monetization requires bulletproof billing workflows and high-converting checkout flows. `saas-launch-revenue` guides the full implementation of payment infrastructure, subscription lifecycles, and automated revenue operations.

## Core Implementation Blueprint

### 1. Checkout & Customer Portal Integration
- Implement Stripe Checkout Sessions (or Mercado Pago Checkout Pro).
- Provide self-serve Customer Portal for upgrading, downgrading, updating credit cards, and cancelling.

### 2. Idempotent Webhook Processing
- Secure webhook endpoints with signature validation (`stripe.webhooks.construct_event`).
- Handle core event hooks:
  - `checkout.session.completed`: Provision user account and assign tier credits.
  - `invoice.payment_succeeded`: Renew subscription cycle and reset monthly usage quota.
  - `invoice.payment_failed`: Trigger dunning sequence, email notification, and grace period.
  - `customer.subscription.deleted`: Downgrade account gracefully to free tier.

### 3. Usage Metering & Quotas
- Enforce server-side rate limits and quota checks before executing paid operations.
- Return structured `402 Payment Required` or `429 Too Many Requests` with upgrade URLs when limits are reached.

### 4. Dunning & Churn Reduction
- Configure smart retries on failed payments.
- Display in-app banner for expiring credit cards or failed payment grace periods.
