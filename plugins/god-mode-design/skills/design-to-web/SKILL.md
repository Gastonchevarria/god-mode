---
name: design-to-web
description: "Turns a Figma design into a polished, accessible web component: exact tokens via the Figma MCP server, pixel-faithful build with every state, spring motion, Playwright verification. Use when the user says /design, 'implement this Figma', 'make it feel native' or 'pixel-perfect'."
---

# Design to Web

You are the bridge between a strict design and the interactive experience people use. The Figma file is the spec; the browser is the proof. Nothing ships on the default state alone, and nothing ships unverified.

## Workflow

Run the four steps in order. Each one has its own skill with the details; this skill is the conductor.

| Step | Skill | Done when |
| --- | --- | --- |
| 1. Extract | `figma-to-code` | A token table (colors, spacing, type, radii, shadows) read from Figma, not guessed, and the layer tree of the component |
| 2. Build | this skill, section below | Semantic, accessible markup with every state implemented |
| 3. Motion | `motion-design` | Springs on interactive elements, staggered entrances, `prefers-reduced-motion` fallback |
| 4. Verify | `ui-states-verification` | Playwright has driven every state and compared it against the Figma screenshot |

Before step 1, confirm the Figma MCP server is connected. If it is not, do not estimate values from a screenshot: stop and show the user how to connect it (see `figma-to-code`). Connecting an MCP server is an external install under the protocol's autonomy limits, so wait for their "yes".

Start the reply with the usual `⚡ GOD` line when invoked through `/god`; otherwise open with the token table from step 1.

## Build standard

- **The design is the law.** Match the extracted tokens exactly: sub-pixel alignment, vertical rhythm, line-height, letter-spacing. Where the design is ambiguous, say so and pick the closest token already in the file instead of inventing one.
- **Semantic and accessible.** Native elements first (`button`, `a`, `input`, `dialog`), then ARIA only to fill gaps. Keyboard reachable, visible `focus-visible` ring, labels and names for assistive tech, color contrast at least 4.5:1 for text.
- **Every state, always.** `default`, `hover`, `active`, `focus-visible`, `disabled`, `loading`, and `error` or `empty` where the component has data. A component delivered with fewer states is unfinished.
- **Touch targets of at least 44×44 px.** When the visual element is smaller, grow the hit area with padding or a pseudo-element, never the visible shape.
- **Composition-only animation.** Animate `transform` and `opacity`; never `width`, `height`, `top`, `left`, `margin` or `box-shadow` on interaction. Promote layers with `will-change` only while they animate.
- **Design-system first.** If the project already has tokens or components, map Figma variables to them instead of hard-coding values. For components with no Figma source, use `frontend-ui-engineering` instead of this skill.

## Deliverable

1. The token table from Figma, with the Figma variable name next to each value.
2. The component, with its states, in the project's framework and styling convention.
3. The motion spec: which elements move, with which spring parameters, and what happens under reduced motion.
4. The Playwright verification: a per-state screenshot set and the checks that passed, with any mismatch against Figma listed on the first line of the reply.

Report what the tools showed. If Figma could not be read, Playwright could not run, or a state failed, that goes first, never in the summary.
