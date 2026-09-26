---
name: launch-growth-loop
description: "Builds product-led growth into the product: landing pages, activation events, referral loops and lifecycle triggers. Use when the user says /growth, 'add a referral loop', 'define our activation event' or 'PLG funnel'. Not for recurring marketing workflows (use marketing-loops)."
---

# Launch & Growth Loop Architecture

## Overview

A great product without distribution dies silently. `launch-growth-loop` integrates distribution and user retention directly into the product codebase, turning every active user and screen into an organic growth engine.

## Core Growth Mechanics

### 1. High-Converting Landing Page Structure
- **Above the Fold**: Clear outcome-based headline + 1-sentence sub-headline + prominent CTA + visual social proof or interactive live demo preview.
- **Problem Agitation**: Visually contrast "The Old Manual Way" vs. "The Automated 10x Way".
- **Interactive Feature Showcases**: Short looping WebP/video demos of the primary AHA! moment.
- **Transparent Pricing with FAQ**: Interactive pricing toggle (Monthly / Annual with 20% discount).
- **Final High-Urgency CTA**.

### 2. The Onboarding Activation Funnel
- Minimize Time-To-First-Value (TTFV): Allow users to test the core value *before* forcing complex setup or credit card input.
- **Activation Milestone**: Define the exact event (e.g. `first_lead_exported`, `first_doc_processed`) that correlates with long-term retention.

### 3. Built-In Virality & Referral Loops
- "Powered by [Product Name]" badges on customer-facing exports, embedded widgets, or shared public links.
- One-click referral invite with reward credit (e.g. +50 bonus AI credits).

### 4. Lifecycle & Retention Triggers
- **Day 0**: Welcome + Quickstart guide.
- **Day 2 (If not activated)**: "Can I help you process your first file?" nudge.
- **Day 7 (If active)**: Feature spotlight on power workflows.
- **Day 14 (Trial ending)**: ROI recap email ("You saved 4.5 hours this week with Pro").

### 5. Programmatic SEO Engine
- Generate clean, fast, indexable landing pages targeting long-tail intent keywords (e.g. `/tools/[use-case]-generator` or `/convert-[format]-to-[format]`).

## Output Format

Save growth architecture in `brain/<conversation-id>/growth_loop_blueprint.md`.
