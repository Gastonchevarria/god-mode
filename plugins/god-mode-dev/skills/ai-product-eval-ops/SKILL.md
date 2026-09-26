---
name: ai-product-eval-ops
description: Establishes continuous evaluation pipelines, ground-truth benchmark datasets, hallucination detection metrics, latency/cost profiling, and regression testing for LLM-powered applications.
---

# AI Product & Evaluation Ops

## Overview

Software with non-deterministic LLMs requires automated evaluation (Evals) to measure accuracy, catch regressions when updating prompts/models, and protect against hallucinations. `ai-product-eval-ops` builds rigorous testing pipelines for AI features.

## Evaluation Framework

### 1. Golden Dataset Creation
- Maintain a curated suite of 50-200 representative input-output test cases in JSONL format.
- Include edge cases: malformed user inputs, adversarial prompts, multi-language requests, empty documents.

### 2. Evaluation Metrics Matrix
- **Exact Match / Schema Validity**: 100% required for structured JSON extraction.
- **Semantic Similarity / Cosine Distance**: Measure fidelity against ground-truth answers (> 0.88 threshold).
- **LLM-as-a-Judge Evaluation**: Use a frontier model to score outputs on:
  1. *Faithfulness / Groundedness* (Is every claim backed by retrieved context?)
  2. *Answer Relevance* (Did it answer the actual question?)
  3. *Completeness* (Did it omit critical details?)

### 3. CI/CD Integration
- Run evaluation suites on pull requests when prompts, model parameters, or retrieval logic are modified.
- Fail build if overall benchmark score degrades by more than 2%.
