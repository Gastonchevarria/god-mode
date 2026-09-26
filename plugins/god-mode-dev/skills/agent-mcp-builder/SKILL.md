---
name: agent-mcp-builder
description: Builds Model Context Protocol (MCP) servers, tools, resources, and prompts with strict JSON schema validation, stdio/SSE transports, error boundaries, and seamless integration with AI coding agents.
---

# Agent & MCP Builder

## Overview

The Model Context Protocol (MCP) provides a standardized protocol for AI models and agents to interact with external tools, databases, APIs, and file systems. `agent-mcp-builder` establishes best practices for building, debugging, and maintaining MCP servers in TypeScript/Node.js and Python.

## Core Architecture

### 1. Transports & Protocols
- **stdio Transport**: Standard input/output for local desktop applications, CLI agents, and IDE extensions.
- **SSE (Server-Sent Events) Transport**: Over HTTP for remote, cloud-hosted MCP services.

### 2. Tools Definition Standard
- Strict JSON Schema parameter definitions with descriptive parameter instructions.
- Clear tool names and human-readable summaries.
- Return structured content blocks (`{ type: "text", text: "..." }` or `{ type: "image", ... }`).

### 3. Error Handling in MCP Tools
- Never crash the MCP server process on tool execution errors.
- Catch internal exceptions and return informative error payloads so the agent can self-correct:
  ```json
  {
    "isError": true,
    "content": [{ "type": "text", "text": "Error: Database connection timed out. Verify DB_HOST configuration." }]
  }
  ```

### 4. Lazy vs. Eager Tool Registration
- For large catalogs (> 10 tools), register tools lazily with lightweight schema manifests to prevent bloating the model's initial context window.
