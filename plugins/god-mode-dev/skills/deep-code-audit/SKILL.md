---
name: deep-code-audit
description: "Audits an entire repository, not a diff: bugs, dead code, TODOs, dummy returns, unfinished endpoints, swallowed errors, missing tests, security, performance. Use when asked to \"audit the whole repo\", \"find incomplete features\" or \"deep code audit\". One diff: code-review-and-quality."
---

# Deep Code Audit Skill

Use this skill when the user asks to "audit the entire repository", "find incomplete features", or "run deep code review".

## 12-Point Audit Methodology

When invoked, act as an expert Hybrid LLM Code Reviewer. You must audit the entire repository (not just recently modified files).

Search for and classify:
1. **Bugs funcionales y errores de lógica**: Flujos que obviamente van a fallar en runtime.
2. **Funciones declaradas pero nunca utilizadas**: Código muerto o huérfano.
3. **TODO, FIXME, HACK y placeholders**: Comentarios que indican deuda técnica.
4. **Rutas, botones o endpoints que no tienen implementación completa**: UI que no hace nada o APIs que devuelven errores 501.
5. **Funciones que retornan valores ficticios**: Funciones mockeadas (`return null`, `return []`, `return {}`, `return true/false`).
6. **Manejo de errores ausente o incompleto**: Promesas sin `catch`, `try/catch` vacíos, o errores tragados silenciosamente.
7. **Flujos que comienzan pero no terminan**: Webhooks sin procesamiento final, procesos en background que mueren.
8. **Integraciones con APIs o bases de datos parcialmente implementadas**: Llamadas de red simuladas.
9. **Variables, componentes y servicios desconectados**: Exports sin import.
10. **Tests faltantes para funcionalidades importantes**: Core business logic sin cobertura.
11. **Problemas de seguridad**: Hardcoded secrets, inyecciones (SQL/NoSQL), XSS, falta de sanitización.
12. **Problemas de rendimiento y fugas de recursos**: N+1 queries, memory leaks, bucles ineficientes, renders innecesarios.

## Format of the Audit Report

For each finding, you MUST provide:
- **Severidad**: Crítica, alta, media o baja.
- **Archivo y número de línea**: Ubicación exacta.
- **Evidencia concreta**: El bloque de código problemático.
- **Por qué es un problema**: Impacto real en la aplicación.
- **Cómo reproducirlo**: Pasos o condiciones para que falle.
- **Solución recomendada**: Código corregido o estrategia de refactor.
- **Requiere un nuevo test**: Sí/No, y por qué.

## Execution Steps for the Agent

1. **Static Analysis**: Run `npm run lint` and `npm run build` (if applicable) to catch dead code and typescript errors.
2. **Grep Scanning**: Use `grep_search` to actively hunt for "TODO", "FIXME", "HACK", "console.log", "return null", "return []", "return true".
3. **Architecture Mapping**: Use `list_dir` to map `src/app`, `src/api`, `src/components`, `src/lib` to find incomplete routes.
4. **Report Generation**: Compile all findings into a comprehensive `audit_report.md` artifact.
