---
name: nextjs-app-router
description: Implements modern Next.js App Router patterns, React Server Components (RSC), Server Actions, Suspense streaming, parallel/intercepting routes, caching strategies, and optimistic client UI updates.
---

# Next.js App Router Patterns

## Overview

Modern Next.js leverages React Server Components (RSC) to minimize client-side JavaScript bundles while providing instant page loads and seamless data fetching. `nextjs-app-router` guides building fast, secure, and maintainable full-stack Next.js applications.

## Key Architecture Patterns

### 1. Server Components by Default
- Keep components on the server (`page.tsx`, `layout.tsx`, static cards, data grids) to fetch data directly without client-side waterfalls.
- Use `'use client'` only at the leaves of the component tree where interactivity, event listeners (`onClick`), or React hooks (`useState`, `useEffect`) are strictly necessary.

### 2. Server Actions for Mutations
- Colocate mutations with Server Actions using `'use server'`.
- Validate all incoming form/JSON payloads using `zod` before executing database writes.
- Return structured result objects `{ success: boolean, data?: T, error?: string }`.
- Trigger `revalidatePath()` or `revalidateTag()` to update cached server data seamlessly.

### 3. Suspense Streaming & Skeleton Loaders
- Wrap slow async data boundaries in `<Suspense fallback={<CardSkeleton />}>` to stream UI chunks immediately to the browser without blocking the initial HTML response.

### 4. Optimistic UI Updates
- Use `useOptimistic` for instantaneous feedback on upvotes, likes, list item additions, and status toggles before server roundtrips finish.
