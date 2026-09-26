---
name: anti-slop
description: Rejects and cleans AI-generated slop, low-evidence patterns, lazy type assertions, and performance-degrading anti-patterns in TypeScript and JavaScript. Triggered by /anti-slop, clean code audits, or when refactoring lazy AI code.
---

# Anti-Slop (High-Evidence Clean TypeScript/JavaScript Standard)

## Overview

AI models frequently generate "AI slop" — code that technically compiles or runs but contains lazy shortcuts, memory traps, and weak architectural habits. `anti-slop` enforces high-evidence, high-signal engineering standards across TypeScript and JavaScript.

Whenever writing, auditing, or refactoring code, strictly enforce these 8 non-negotiable rules:

---

## The 8 Non-Negotiable Anti-Slop Rules

### 1. `no-chained-type-assertions` (`x as unknown as Y`)
- **The Slop**: Forcing a type by double-casting (`data as unknown as User`). This blinds the compiler and masks breaking schema drifts.
- **The Fix**: Use runtime validation (Zod, Valibot), proper narrowing with type guards (`if ('id' in data)`), or write an explicit mapper.

### 2. `no-reduce-accumulator-copy` (`{ ...acc, [key]: value }`)
- **The Slop**: Cloning the accumulator object inside `.reduce()` on every single iteration.
  ```ts
  // ❌ ANTI-PATTERN: O(N²) memory churn and GC spikes
  items.reduce((acc, item) => ({ ...acc, [item.id]: item }), {});
  ```
- **The Fix**: Mutate the accumulator in-place inside the reduce loop, or use `Object.fromEntries()` or `new Map()`:
  ```ts
  // ✅ CLEAN & O(N) FAST
  items.reduce((acc, item) => {
    acc[item.id] = item;
    return acc;
  }, {} as Record<string, Item>);
  ```

### 3. `no-array-filter-map` (`.filter(Boolean).map(...)`)
- **The Slop**: Chaining multiple array iterations to filter out nulls/falsy values before mapping.
- **The Fix**: Use a single `.flatMap()` or standard `for...of` loop to transform and filter in a single pass without intermediate throwaway arrays.

### 4. `no-conditional-empty-object-spread` (`...(cond ? { a: 1 } : {})`)
- **The Slop**: Inlining ternary empty object spreads inside object literals. It forces V8 to constantly recompute hidden classes.
- **The Fix**: Construct objects with explicit conditional assignments or builder patterns.

### 5. `no-shape-in-symbol-names` (`userListArray`, `configObject`, `userModel`)
- **The Slop**: Embedding data structure types in variable or parameter names.
- **The Fix**: Name variables after domain concepts: `users`, `config`, `user`.

### 6. `no-unsafe-dictionary-type` (`Record<string, any>` / `any`)
- **The Slop**: Passing unconstrained loose objects across module boundaries.
- **The Fix**: Define strict interfaces with optional or discriminated union properties.

### 7. `require-safety-comment-for-type-assertion`
- **Rule**: If an `as T` cast is strictly required (e.g. interfacing with untyped DOM or legacy APIs), you **MUST** precede it with a single-line comment explaining *why* it is guaranteed safe:
  ```ts
  // Safe: canvas ref is verified mounted in useEffect before calling getContext
  const ctx = canvasRef.current.getContext("2d") as CanvasRenderingContext2D;
  ```

### 8. `no-module-mocking` (in tests)
- **The Slop**: Over-mocking entire modules with `vi.mock()` or `jest.mock()`, leaving tests detached from real behavior.
- **The Fix**: Prefer dependency injection, in-memory test doubles, or MSW (Mock Service Worker) for network boundaries.

---

## When to Use

- When reviewing a PR or feature before merge.
- When cleaning up code generated during high-speed prototyping.
- Triggered by `/anti-slop`, "audita el código contra anti-slop", or automatically during `/thermos`.
