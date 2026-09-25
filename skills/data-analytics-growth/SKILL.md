---
name: data-analytics-growth
description: Implements product analytics, client/server telemetry tracking, conversion funnel measurement, cohort retention tracking, and A/B experimentation frameworks (PostHog, Mixpanel, Custom Events).
---

# Data Analytics & Growth Telemetry

## Overview

You cannot optimize what you do not measure. `data-analytics-growth` embeds standardized telemetry and conversion tracking into web apps, backend APIs, and landing pages to monitor user engagement and growth funnels.

## Telemetry Standard

### 1. Unified Event Taxonomy
- Format: `[Object] [Action]` (e.g. `user_signed_up`, `document_uploaded`, `extraction_completed`, `checkout_started`, `subscription_upgraded`).
- Every event must include standard metadata:
  ```json
  {
    "userId": "usr_12345",
    "timestamp": "2026-08-10T01:46:00Z",
    "plan": "pro",
    "source": "web_dashboard",
    "properties": {
      "fileType": "pdf",
      "fileSizeKb": 420,
      "durationMs": 1340
    }
  }
  ```

### 2. The 4 Vital Funnels
1. **Acquisition Funnel**: Landing Page View -> Click CTA -> Sign Up Completed.
2. **Activation Funnel**: Sign Up -> Onboarding Step 1 -> Core Action / Value Moment (TTFV).
3. **Monetization Funnel**: Reached Usage Limit -> Click Upgrade -> Checkout Completed.
4. **Retention Funnel**: Active in Week 0 -> Active in Week 1 -> Active in Week 4.
