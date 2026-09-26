---
name: plan-design-review
description: Evaluates and elevates UX/UI design, information hierarchy, emotional resonance, design tokens, micro-interactions, and eliminates generic AI-generated aesthetics. Use before writing frontend code.
---

# Plan Design Review (UX/UI & Anti-AI Aesthetics)

## Overview

Software that looks generic, template-driven, or AI-generated destroys trust and kills conversion. The `plan-design-review` reviews proposed user journeys and visual interfaces, ensuring every screen feels handcrafted, premium, lightning-fast, and intuitively designed.

## When to Use

- When designing new screens, dashboards, landing pages, or onboarding flows.
- Before implementing React/Next.js/HTML components.
- When fixing UX friction, confusing layouts, or low conversion rates.

## The 6 Anti-Generic Design Principles

1. **Curated Color Palettes (No Raw Primaries)**:
   - Reject default blues (`#0000FF`), harsh pure blacks (`#000000`), or flat grays.
   - Use nuanced HSL color systems, subtle dark mode elevation layers (`#0d1117` -> `#161b22` -> `#21262d`), and luminous accent gradients.
2. **Typography Hierarchy with Intent**:
   - Modern, readable typography (Inter, Outfit, Plus Jakarta Sans, JetBrains Mono for data/code).
   - Clear size and weight contrasts (`h1` 32-40px bold, `h2` 24px semibold, `body` 14-16px 400/500).
3. **Micro-Interactions & State Polish**:
   - Hover states, active press transforms (`scale(0.98)`), smooth skeleton loaders instead of jarring spinners.
   - Fluid transitions (150-250ms ease-out).
4. **Information Architecture & Density**:
   - Progressive disclosure: show essential summaries first; reveal details on expand/click.
   - Generous spacing (8pt grid system: 8px, 16px, 24px, 32px, 48px).
5. **Zero Placeholders**:
   - High-fidelity realistic sample data that mirrors actual production usage.
6. **Mobile Responsiveness & Touch Targets**:
   - Minimum 44x44px touch targets on mobile viewports.

## Output Format

Save the Design review in `brain/<conversation-id>/design_review.md`:

```markdown
# Design Review: [Feature/Screen Name]

## 1. Visual Theme & Token Foundation
- **Theme**: [Sleek Dark Mode / Clean High-Contrast Light / Hybrid]
- **Primary Accent**: [e.g., Violet-Indigo Glow / Emerald Neon / Electric Amber]
- **Font Stack**: [Heading / Body / Monospace]

## 2. Screen Breakdown & Layout Hierarchy
- **Primary Viewport**: [Desktop 1280px+ / Mobile 390px]
- **Key Visual Anchors**: [Hero Metric, Primary CTA, Interactive Canvas]
- **Empty States & Skeletons**: [Defined behavior when data is 0]

## 3. Micro-Interactions & Transitions
- [Button hover, modal entrance, toast notifications, drawer slide]

## 4. Accessibility & Contrast Audit
- WCAG AA compliant contrast ratios (4.5:1 text, 3:1 graphical elements).
```
