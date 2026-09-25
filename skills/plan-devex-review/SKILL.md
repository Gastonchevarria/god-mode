---
name: plan-devex-review
description: Evaluates developer experience, API ergonomics, SDK/CLI usability, configuration simplicity, setup friction, and documentation clarity. Use when building APIs, developer tools, libraries, or internal frameworks.
---

# Plan DevEx Review (Developer Experience & Ergonomics)

## Overview

When building developer tools, public APIs, SDKs, or shared internal libraries, developer experience (DevEx) dictates adoption. If an API is cumbersome, confusing, or poorly typed, developers abandon it.

`plan-devex-review` reviews code interfaces from the consumer developer's perspective, optimizing for minimal time-to-first-hello-world and intuitive ergonomics.

## When to Use

- When designing public or internal REST/GraphQL APIs, MCP tools, or SDKs.
- When creating CLI tools or automation scripts.
- When drafting developer documentation and code examples.

## Key Principles of Elite DevEx

1. **Zero-Config Defaults, Infinite Customizability**:
   - Simple tasks must take 3 lines of code; complex tasks should remain possible.
2. **Predictable Naming & Typing**:
   - Strict TypeScript/Pydantic types with informative IDE autocomplete and inline docstrings.
3. **Actionable Error Messages**:
   - Never return generic `Error: Invalid argument`.
   - Always return: `Error: Missing 'apiKey'. Set the ANTHROPIC_API_KEY environment variable or pass { apiKey: '...' } in config.`
4. **Copy-Paste Ready Examples**:
   - Every API endpoint or method must have a working, copy-pasteable snippet.

## Output Format

Save in `brain/<conversation-id>/devex_review.md`:

```markdown
# DevEx Review: [Tool/API Name]

## 1. Ergonomics & Interface Assessment
- **Time to First Success**: [< 2 minutes target]
- **Type Safety**: [Strict TypeScript types / Pydantic models]

## 2. Error Message Quality Audit
- Example Error: `[Descriptive error with fix suggestion]`

## 3. Quickstart Snippet
```typescript
// Verified minimal example
```
```
