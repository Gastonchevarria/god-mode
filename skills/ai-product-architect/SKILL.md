---
name: ai-product-architect
description: Architect production-grade AI systems, LLM inference pipelines, model selection, prompt token optimization, latency budgets, streaming UX, semantic caching, RAG architecture, eval harnesses, and prompt injection security. Triggered by /ai-arch, /llm-arch, /rag-arch, or when designing AI product architectures.
---

# AI Product Architect

## Overview

Building production AI software is completely different from running a demo script. Real-world AI applications must navigate non-deterministic outputs, API latencies, token economics, hallucinations, and prompt injections.

`ai-product-architect` provides the blueprint for building reliable, fast, cost-efficient, and secure AI-native products.

## The 8 Principles of Production AI Architecture

1. **AI vs. Deterministic Code Boundary**:
   - Never use an LLM for operations that regex, AST parsing, or deterministic algorithms can do for free in 1 millisecond.
2. **Multi-Tier Model Routing**:
   - Tier 1: Fast/cheap models (Gemini Flash, Claude Haiku, GPT-4o-mini) for classification, routing, and simple extraction.
   - Tier 2: Frontier models (Gemini Pro, Claude Sonnet, GPT-4o) only for complex synthesis, deep reasoning, or code generation.
3. **Latency Optimization & Streaming UX**:
   - Stream tokens immediately to the frontend (`ReadableStream` / Server-Sent Events).
   - Optimistic UI updates with micro-skeletons while first token generates (TTFT < 800ms).
4. **Smart Caching Layers**:
   - Exact match cache (SHA256 of prompt + parameters in Redis).
   - Semantic cache (vector similarity cosine distance > 0.96) for repetitive user inquiries.
5. **RAG (Retrieval-Augmented Generation) Architecture**:
   - Chunking: Semantic or recursive chunking (500-1000 tokens with 10% overlap).
   - Hybrid Search: Dense vectors (embeddings) + Sparse BM25 keyword search.
   - Re-ranking: Cross-encoder re-ranking for top 5 retrieved contexts.
6. **Structured Output & Schema Enforcement**:
   - Strict JSON Schema / Pydantic validation on model responses.
   - Automatic 1-shot repair retry loop if output schema fails validation.
7. **Security & Guardrails**:
   - Sanitize untrusted input against indirect prompt injections and jailbreaks.
   - PII masking on outbound API calls.
8. **Evals & Continuous Monitoring**:
   - Ground-truth evaluation harness with automated scoring on precision, recall, and hallucination rate.

## Output Format

Save the technical blueprint in `brain/<conversation-id>/ai_system_architecture.md`.
