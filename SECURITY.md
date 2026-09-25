# 🛡️ Security Policy — DEV GOD-MODE

The **DEV GOD-MODE** engineering squad takes the security of autonomous development, prompt safety, and developer workstation environments seriously. This document outlines our security practices, supported versions, and how to responsibly disclose vulnerabilities.

---

## 📦 Supported Versions

We actively provide security patches, threat mitigations, and dependency updates for the following versions:

| Version | Supported | Description |
| :--- | :---: | :--- |
| **1.x / `main`** | ✅ | Current active release (DEV GOD-MODE + Fable 5.1 Protocol) |
| **< 1.0** | ❌ | Deprecated / unmaintained |

---

## 🔒 Security Architecture & AI Agent Safeguards

DEV GOD-MODE injects high-autonomy instructions into LLM engines (Claude Code, Cursor, Antigravity, Windsurf). To protect developers, our architecture enforces strict security principles:

### 1. Zero Credential Exfiltration (Air-Tight Secrets Rule)
- **Rule Enforcement**: Core instructions explicitly forbid AI agents from ever displaying, printing, logging, committing, or passing private keys, `.env` variables, seed phrases, or cloud tokens (`AWS_*`, `OPENAI_*`, `ANTHROPIC_*`, `BINANCE_*`, etc.) into output artifacts or git commits.
- **Git Protection**: The default `.gitignore` and CLI installers prevent accidental commits of local secrets, bash histories, or cache directories.

### 2. Sandboxing & Safe Execution
- **Least Privilege**: The CLI (`god-mode`) and installer run purely in user space (`$HOME/.local/bin` and `$HOME/.claude`). They **never require nor request `sudo` permissions**.
- **Sandbox Compliance**: Subagents and skills respect the execution sandbox of Claude Code and Antigravity. Destructive shell commands (e.g. `rm -rf /`, force-pushes, database wipes) require explicit user confirmations.

### 3. Prompt Injection & Anti-Slop Defenses
- Skills and subagent prompts are architected with strict boundary isolation, preventing indirect prompt injection attacks from malicious repositories or third-party web content.
- The `anti-slop` compiler automatically audits and strips out suspicious, obfuscated, or lazy AI hallucinations from generated code.

### 4. Zero Telemetry & Privacy
- **100% Local**: DEV GOD-MODE contains **no telemetry, no tracking pixels, and no phone-home servers**.
- All skill executions, subagent orchestrations, and context updates happen locally on your machine or inside your authenticated AI provider session.

---

## 🚨 Reporting a Vulnerability

If you discover a potential security vulnerability within DEV GOD-MODE (such as a prompt injection escape, credential leak vector, or installer flaw), please **do not open a public GitHub issue**.

### How to Report

1. **GitHub Private Security Advisory (Recommended)**:
   - Navigate to the [Security Advisories](https://github.com/Gastonchevarria/god-mode/security/advisories) tab of this repository.
   - Click **"Report a vulnerability"** to submit an encrypted, private report.

2. **Direct Contact**:
   - If you cannot use GitHub Advisories, contact the maintainer directly via GitHub profile: [@Gastonchevarria](https://github.com/Gastonchevarria).

### What to Include in Your Report
To help us triage and patch the issue quickly, please include:
- A clear description of the vulnerability and its potential impact.
- Step-by-step reproduction steps or a minimal Proof of Concept (PoC).
- The platform and agent engine affected (Claude Code, Cursor, Antigravity, or CLI).
- Any suggested fixes or mitigations if you have them.

---

## ⏱️ Response Timelines & SLA

We are committed to rapid response and transparent resolution:
- **Acknowledgment**: Within 48 hours of initial report.
- **Initial Assessment**: Within 5 business days, confirming vulnerability scope and severity.
- **Security Release**: Critical patches are merged directly into `main` and tagged immediately.
- **Public Disclosure**: Coordinated after the fix has been published and users have had reasonable time to run `god-mode update`.

---

## 💡 Developer Best Practices

When operating autonomous AI coding agents:
1. **Never pass production keys in prompts**: Use local environment variables or secrets managers.
2. **Review git diffs before merging**: Use `/thermos` to perform a double thermo-nuclear review of any PR.
3. **Keep your suite updated**: Run `god-mode update` regularly to pull the latest security rules and skill definitions.

Thank you for helping keep the autonomous AI developer community safe! 🚀
