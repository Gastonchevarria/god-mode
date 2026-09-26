---
name: prompt-engineering-patterns
description: Master prompt engineering strategies including chain-of-thought, few-shot demonstration calibration, strict JSON schema output constraints, system prompt modularity, and context window optimization.
---

# Prompt Engineering Patterns

## Overview

Prompt engineering is the precision programming of foundation models. `prompt-engineering-patterns` provides systematic structures to eliminate hallucinations, enforce rigid JSON output formats, and minimize token overhead.

## Core Prompting Patterns

### 1. The Role-Context-Constraint-Format Structure
Structure prompts into 4 distinct semantic blocks:
```text
<role>
You are an expert financial analyst specializing in SaaS unit economics.
</role>

<context>
The user operates a B2B SaaS with $45k MRR and 120 paying accounts.
</context>

<instructions>
1. Calculate the ARPU and identify expansion revenue opportunities.
2. Highlight any metric exceeding standard churn benchmarks.
</instructions>

<constraints>
- Do NOT guess or hallucinate missing data; flag it explicitly.
- Output ONLY valid JSON matching the schema below.
</constraints>

<output_schema>
{ ... }
</output_schema>
```

### 2. Calibrated Few-Shot Demonstrations
- Provide 2-3 minimal, representative input/output pairs demonstrating the exact format, edge case handling, and tone desired.

### 3. XML Delimiters for Untrusted Content
- Wrap user-provided text or third-party web scrapes in `<untrusted_content>` tags to prevent prompt injection and instruction override attacks.
