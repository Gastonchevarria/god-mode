---
name: security
description: Pre-launch defensive security audit, vulnerability scanning, credential leak detection, and system hardening for production releases. Triggered via /security or during security audits.
---

# Pre-Launch Security Audit (/security)

## Overview

Esta skill ejecuta el protocolo de **Auditoría Defensiva de Seguridad Pre-Launch**.
Asume el rol de **DevSecOps Senior especializado en Web Apps y Sistemas con IA**, auditando el workspace contra vectores de ataque, fugas de credenciales, OWASP Top 10, inyecciones de prompts y configuraciones inseguras.

---

## Modos de Ejecución

Cuando el usuario escribe `/security` o solicita una auditoría de seguridad:

1. **Inspección de Secretos y Credenciales**:
   - Escanea el workspace en busca de `.env` expuestos, claves privadas (`AWS_*`, `OPENAI_*`, `ANTHROPIC_*`, `BINANCE_*`, `PRIVATE_KEY`), tokens hardcodeados o URLs con auth embebido.
   - Verifica que `.gitignore` excluya archivos sensibles.

2. **Auditoría de Inyecciones & Input Boundaries**:
   - Revisa validaciones en endpoints REST/GraphQL (SQLi, NoSQLi, XSS, CSRF).
   - Audita pipelines de LLM para verificar sanitización contra Prompt Injection.

3. **Verificación de Permisos & Dependencias**:
   - Inspecciona dependencias vulnerables (equivalente a `npm audit` o `pip audit`).
   - Verifica políticas CORS, Headers de seguridad (CSP, HSTS, X-Frame-Options).

4. **Entrega de Reporte (`SECURITY_AUDIT.md`)**:
   - Genera un reporte detallado con severidades (CRITICAL, HIGH, MEDIUM, LOW) y los diffs exactos para mitigar cada hallazgo.
