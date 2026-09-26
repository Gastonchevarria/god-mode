---
name: rag-implementation
description: Designs and implements advanced Retrieval-Augmented Generation (RAG) pipelines, semantic/hybrid search (vector + BM25), dense reranking, contextual chunking, metadata filtering, and hallucination reduction.
---

# Advanced RAG Implementation

## Overview

Basic naive RAG (fixed-length chunking + single vector similarity search) produces irrelevant context, hallucinations, and high latency. `rag-implementation` builds production-grade retrieval engines with high precision and verifiable citations.

## The Production RAG Pipeline

```text
[Document Ingestion]
        ↓
1. Document Parsing & Structure Extraction (Headers, Tables, Metadata)
        ↓
2. Contextual Chunking (Semantic boundaries, 500-1000 tokens with 10% overlap)
        ↓
3. Dual Indexing (Dense Embeddings + Sparse BM25 Keywords + Metadata Filters)
        ↓
[User Query] -> Query Rewriting & Expansion
        ↓
4. Hybrid Retrieval (Top 25 Dense + Top 25 Sparse)
        ↓
5. Cross-Encoder Re-Ranking (Select Top 3 - 5 most relevant passages)
        ↓
6. Prompt Synthesis with Grounded Citations -> LLM Streaming Response
```

## Implementation Standards

- **Metadata Enrichment**: Store `source_file`, `page_number`, `section_title`, and `created_at` alongside each chunk vector.
- **Contextual Compression**: Strip out noisy boilerplate before passing chunks into the LLM context.
- **Citation Requirement**: Prompt the model to cite exact chunk IDs `[Source 1, Page 3]` for every factual claim.
