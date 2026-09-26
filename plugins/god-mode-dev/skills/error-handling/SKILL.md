---
name: error-handling
description: Guides the agent to write robust Python and TypeScript code by applying error handling best practices, timeouts, and graceful shutdown patterns. Trigger this implicitly whenever writing code that interacts with external services, files, or network requests.
---

# Robust Error Handling (Python / TypeScript)

When writing or refactoring code in Python or TypeScript, especially code that deals with I/O, network requests, or long-running processes, you MUST prioritize robustness and apply the following patterns:

## 1. Always Clean Up (try/finally)
Ensure that resources (files, network connections, sessions, clients) are always closed properly.
- **Python**: Use `try/finally` blocks or context managers (`with`).
- **TypeScript**: Use `try/finally` blocks.

## 2. Handle Specific Errors
Do not blindly catch generic exceptions unless it's a top-level fail-safe.
- **Python**: Catch `FileNotFoundError`, `ConnectionError`, `TimeoutError`, etc., before `Exception`.
- **TypeScript**: Check the `error.message` or `error.code` (e.g., `ENOENT`, `ECONNREFUSED`) to handle known failure states gracefully.

## 3. Set Appropriate Timeouts
Never make synchronous or asynchronous calls to external services or long-running processes without setting a timeout.
- Use timeout arguments in APIs when available.
- If not available, use `asyncio.wait_for` (Python) or `Promise.race` with a timeout promise (TypeScript).

## 4. Graceful Shutdown
Long-running scripts should handle interruption signals (e.g., `SIGINT`) to clean up before exiting.
- **Python**: Use the `signal` module to catch `signal.SIGINT` and trigger cleanup tasks.
- **TypeScript**: Use `process.on("SIGINT", ...)` to await cleanup before `process.exit(0)`.

## 5. Log Errors
Always capture and log error details (and stack traces when necessary) for debugging. Don't swallow errors silently.
