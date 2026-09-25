---
name: backend-architect
description: Guides scalable backend architecture, database schema design, caching topologies (Redis), message queues (Celery/BullMQ/Kafka), webhook delivery systems, and rate limiting strategies.
---

# Backend Architect (Scalable Backend Systems)

## Overview

A resilient backend balances compute speed, database throughput, and asynchronous background operations. `backend-architect` provides the system design blueprints for high-throughput, fault-tolerant web applications and APIs.

## Core Architectural Patterns

### 1. Database Indexing & Query Optimization
- Index all foreign keys, query filters (`WHERE status = 'active'`), and composite sort columns (`WHERE user_id = X ORDER BY created_at DESC`).
- Prevent N+1 query antipatterns using eager loading (`select_related` / `joinedload` / Prisma `include`).

### 2. Multi-Layer Caching (Redis)
- **Cache-Aside Pattern**: Read from cache -> If miss, fetch DB -> Write to cache with TTL.
- **Cache Invalidation**: Event-driven invalidation on data mutation rather than relying solely on high TTLs.

### 3. Asynchronous Worker & Queue Topology
- Decouple user-facing web request threads from heavy operations: PDF extraction, video processing, LLM generation, batch emails.
- Push jobs to background queues with retry policies, backoff multipliers, and Dead Letter Queues (DLQ).

### 4. Webhook Ingestion & Egress
- **Ingress**: Validate HMAC signature -> Store raw payload in DB -> Enqueue async processing job -> Return `200 OK` in < 50ms.
- **Egress**: Sign payload with HMAC SHA256 -> Deliver with exponential retry schedule (30s, 2m, 15m, 1h, 24h).
