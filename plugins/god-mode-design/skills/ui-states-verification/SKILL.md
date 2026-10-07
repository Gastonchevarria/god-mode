---
name: ui-states-verification
description: "Verifies a rendered component with Playwright: drives hover, focus-visible, active, disabled, loading and error, screenshots each state against the reference image, checks touch targets, reduced motion and a11y. Use when the user says 'verify the states' or 'does it match the design'."
model: claude-opus-5-5
context: fork
---

# UI States Verification

A component is done when a browser has shown every state and each one matches the design. This skill produces that proof with Playwright and reports what the browser showed, not what the code intends.

## Setup

Use whatever Playwright the project already has (`@playwright/test` in `package.json`, or the Playwright MCP server if the session exposes `browser_navigate` and `browser_take_screenshot`). If neither exists, propose one and wait for the user's "yes" before installing; adding a dependency is an external install:

```bash
npm i -D @playwright/test && npx playwright install chromium
# or, as an MCP server for the agent itself:
claude mcp add playwright -- npx @playwright/mcp@latest
```

Render the component in isolation when possible: the project's Storybook, a dev route, or a small HTML harness under a scratch directory. Fix the viewport (for example 1280×800 and 390×844) and disable animations only for the pixel comparison, never for the state checks.

## The state matrix

Drive every state and capture it. Skip a row only if the component has no such state, and say so.

| State | How to drive it | Capture |
| --- | --- | --- |
| default | load | screenshot |
| hover | `locator.hover()` | screenshot |
| focus-visible | `page.keyboard.press('Tab')` until focused (never `locator.focus()`, which may not show the ring) | screenshot + assert the ring is visible |
| active | `page.mouse.down()` without `up()` | screenshot mid-press |
| disabled | render with the disabled prop | screenshot + assert not clickable and not in tab order |
| loading | render with the loading prop | screenshot + assert the control is inert while loading |
| error / empty | render with the error or empty data | screenshot |
| reduced motion | `page.emulateMedia({ reducedMotion: 'reduce' })` | re-run the entrance and assert no transform animation runs |

## Checks beyond screenshots

- **Fidelity.** When the request includes a reference image (a mockup or screenshot saved in the project), compare each screenshot against it with a pixel diff at the same viewport; tolerate anti-aliasing (threshold around 0.2 per pixel), nothing else, and list every diff region in the reply. A mockup is not a render of the same code, so report the diff regions instead of failing on them. Without a reference image, skip this check and say so.
- **Touch targets.** For each interactive element, `boundingBox()` is at least 44×44 px; when the visual is smaller, the hit area (padding or pseudo-element) still reaches 44.
- **Keyboard.** Tab order follows the visual order; `Enter` and `Space` activate buttons; `Escape` closes overlays.
- **Accessibility.** Run an axe scan (`@axe-core/playwright`) and treat serious or critical issues as failures. Check the accessible name of each control.
- **Motion.** Read `getComputedStyle(el).transitionProperty` and `animationName` on interactive elements: only `transform` and `opacity` may animate. Under reduced motion, spatial animations must be gone.
- **Performance smell.** During hover and press, no layout-affecting property changes (`width`, `height`, `top`, `left`); a `MutationObserver` or a before/after `boundingBox()` comparison catches it.

## Report

First line: pass or the first failure. Then the matrix with one row per state and its result, the diff regions against the reference image, and the screenshot paths. A failed state is not "minor": either fix it and re-run, or hand it back to the build step with the screenshot that shows it.
