---
name: fastapi-pro
description: Guides development of high-performance asynchronous FastAPI applications with Pydantic v2 schemas, dependency injection, structured error handling, background tasks, and production OpenAPI documentation.
---

# FastAPI Pro (Production-Ready Async Python)

## Overview

FastAPI is the standard for high-performance Python backends and AI microservices. `fastapi-pro` enforces modern asynchronous best practices, clean layered architecture, and robust type safety with Pydantic v2.

## Architectural Best Practices

### 1. Clean Layered Architecture
```text
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/       # Route handlers (thin controllers)
│   │   └── router.py        # Centralized APIRouter aggregation
│   └── deps.py              # Reusable Depends() providers (Auth, DB session, Client)
├── core/
│   ├── config.py            # Pydantic BaseSettings with .env validation
│   ├── errors.py            # Global exception handlers
│   └── security.py          # JWT, hashing, API key verification
├── models/                  # SQLAlchemy / SQLModel database entities
├── schemas/                 # Pydantic v2 request / response models
├── services/                # Pure business logic and LLM orchestration
└── db/                      # Engine, sessionmaker, migrations (Alembic)
```

### 2. Modern Pydantic v2 Patterns
- Always use `model_config = ConfigDict(from_attributes=True, populate_by_name=True)`.
- Explicit request/response typing on all endpoints: `response_model=CustomResponseSchema`.

### 3. Asynchronous Best Practices
- Never use blocking synchronous I/O inside `async def` route handlers (e.g. `requests.get()`, `time.sleep()`).
- Use `httpx.AsyncClient` or `aiohttp` for non-blocking HTTP requests.
- For heavy CPU-bound tasks, offload to `asyncio.to_thread` or background task queues (Celery/ARQ/BullMQ).
