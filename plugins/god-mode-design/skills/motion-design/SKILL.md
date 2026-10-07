---
name: motion-design
description: "Implements UI motion in code: spring transitions, press feedback, staggered entrances, skeletons and a prefers-reduced-motion fallback, on transform and opacity only. Use when the user says 'add animations', 'it feels stiff', 'spring animation' or 'microinteractions'."
---

# Motion Design

Motion is feedback, not decoration. Every animation answers one of three questions for the user: what did I just do, where did this come from, or what is happening now. If it answers none, leave it out.

## Start from the direction

Before choosing springs, settle what the motion should feel like with `motion-direction` (LottieFiles' motion principles): one personality for the whole product (Playful, Premium, Corporate or Energetic), its duration palette and signature easing, the stagger budget, and which element leads. This skill then builds that direction with the rules below.

When the two disagree, this skill wins on three points:

- **Properties.** Only `transform` and `opacity` animate on interaction. A shadow that "arrives 50 ms after the card" is a pseudo-element whose `opacity` animates, not an animated `box-shadow`.
- **Reduced motion.** Under `prefers-reduced-motion: reduce`, motion becomes opacity-only, even where `motion-direction` says state changes need position or scale.
- **Ambient layer.** Controls (buttons, inputs, menus, forms) get no looping background motion. Ambient motion belongs to heroes and illustrations, and anything that loops over 5 seconds needs a pause control.

Map the personality to springs with the table in "Spring reference": Premium and Corporate use the no-overshoot rows, Playful and Energetic the ones with a bounce.

## Rules

1. **Springs for interaction, not easing curves.** Elements the user touches (buttons, toggles, sheets, drag handles) move with spring physics, so they respond to the user's energy and settle naturally. Reserve `ease-out` for things the user did not cause, such as a toast appearing.
2. **Immediate press feedback.** Pressing a button scales it to about `0.97`–`0.95` and releasing springs it back. The feedback starts on `pointerdown`, not on `click`.
3. **Stagger entrances.** When several elements appear together (list items, cards, menu options), delay each by 30–50 ms. Cap the stagger: after about 8 items, the rest appear together, or the user waits for the list.
4. **Composition properties only.** Animate `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`, `padding`, `margin`, `box-shadow` or `filter` on interaction; they trigger layout or paint on every frame. For a size change, animate a clip or a `scale` and counter-scale the children, or use the FLIP technique.
5. **Durations.** Micro feedback 100–200 ms; small element transitions 200–300 ms; page-level movement 300–500 ms. Exit animations shorter than entrances. Nothing on the interaction path over 500 ms.
6. **Reduced motion is a first-class state.** Under `prefers-reduced-motion: reduce`, replace spatial movement (slide, scale, bounce) with opacity-only transitions of 150 ms or less. Keep the state change itself; only the motion goes.
7. **Interruptible.** A spring that is mid-flight retargets when the user acts again; it never waits to finish. CSS transitions already do this; with a JS spring library, feed the new target instead of restarting.
8. **Loading states move slowly.** Skeletons shimmer over 1.2–1.6 s with a soft gradient; spinners never appear for waits under 300 ms (show nothing, then the skeleton).

## Spring reference

| Use | Stiffness | Damping | Mass | Feels like |
| --- | --- | --- | --- | --- |
| Button press and release | 400–600 | 25–35 | 1 | Snappy, no overshoot |
| Toggle, checkbox, chip | 300–400 | 20–28 | 1 | Quick with a hint of bounce |
| Sheet, drawer, modal | 200–300 | 25–30 | 1 | Weighted, settles once |
| Drag release, swipe | 150–250 | 15–22 | 1 | Carries momentum, one overshoot |

CSS has no spring primitive, so pick one of these, in order of preference:

- **CSS `linear()` easing** generated from the spring parameters (one function per spring, no runtime cost). Good for hover, press and most entrances.
- **The project's animation library**, when it already has one (Framer Motion / Motion for React, React Spring, Vue Motion). Use its spring API with the parameters above; do not add a second library.
- **A small spring in JS** driving `transform` through `requestAnimationFrame`, only for gestures that need live retargeting (drag, swipe to dismiss).

## Press feedback, the minimal version

```css
.button {
  transition: transform 180ms linear(0, 0.3, 0.7, 0.95, 1.02, 1);
}
.button:active { transform: scale(0.96); }

@media (prefers-reduced-motion: reduce) {
  .button { transition: none; }
}
```

The `linear()` points above approximate a stiff spring; generate exact points from the parameters when the project has a build step, and keep the generator with the tokens.

## Stagger, the minimal version

```css
.list > * {
  animation: enter 240ms linear(0, 0.4, 0.8, 0.98, 1) both;
  animation-delay: calc(var(--i) * 40ms);
}
@keyframes enter {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}
@media (prefers-reduced-motion: reduce) {
  .list > * { animation: fade 120ms ease-out both; }
  @keyframes fade { from { opacity: 0 } to { opacity: 1 } }
}
```

Set `--i` per item from the markup or the framework; do not generate one class per index.

## Motion spec to hand to verification

For every animated element write one line: element · trigger · properties · spring or duration · reduced-motion fallback. `ui-states-verification` turns these lines into checks, including the reduced-motion run.
