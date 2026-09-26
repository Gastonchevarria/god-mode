---
name: god
description: "Routes a request to the right god-mode skills and subagents and runs it end to end under the Fable 5.1 Protocol. Use when the user types /god or asks for 'full autonomous mode' or 'handle this end to end'. Not for ordinary single-skill requests; use that skill directly."
---

# DEV GOD-MODE Router (El Orquestador Maestro Inteligente — Fable 5.1 Tier)

## Overview

El comando `/god` es el **Meta-Comando Inteligente y Orquestador Maestro** de la suite DEV GOD-MODE. Analiza cualquier mensaje, problema o duda que plantees, diagnostica en qué fase técnica o de producto te encuentras y activa automáticamente la mejor combinación de herramientas, subagentes y skills sin que tengas que recordar los nombres técnicos.

Opera bajo el estándar **Fable 5.1**, combinando la autonomía implacable de Claude Code/Fable 5.1, la precisión en código de Cursor y el rigor estético y arquitectónico de Antigravity.

---

## Protocolo Fable 5.1

Antes de ejecutar cualquier ruta, leé [`references/protocol.md`](references/protocol.md) y aplicalo durante toda la tarea. Sus **Límites de autonomía** tienen prioridad sobre cualquier otra regla: push, deploys, borrados, migraciones, dinero o credenciales, mensajes a terceros e instalaciones externas requieren un "sí" explícito del usuario.

---

## Regla de Comunicación Obligatoria (Transparencia Total)

> [!IMPORTANT]
> **REGLA CRÍTICA PARA EL AGENTE**: 
> Cada vez que se active `/god`, **DEBES EMPEZAR TU RESPUESTA CON UNA LÍNEA QUE MUESTRE LA RUTA Y LAS SKILLS ELEGIDAS** antes de realizar herramientas complejas o en silencio:
> 
> ```markdown
> ⚡ **GOD** · Ruta: [ruta elegida] · Skills: [skills que se activan] · [qué se va a hacer, en una frase]
> ```
>
> Una sola línea: el diagnóstico largo va solo si el usuario lo pide.

---

## Matriz de Ruteo Inteligente

```text
[Input del Usuario]
       │
       ▼
¿En qué fase o problema estás?
 ├── 💥 "¿Quiero una auditoría implacable pre-merge / Thermo-Nuclear Review de un branch/diff?"
 │    └── Ruta: THERMO-NUCLEAR REVIEW ➔ Activa `thermos` (`thermo-nuclear-review` + `thermo-nuclear-code-quality-review`)
 │
 ├── 🧹 "¿Quiero auditar y eliminar vicios, código vago y anti-patrones de IA en TypeScript/JS?"
 │    └── Ruta: ANTI-SLOP CLEAN CODE ➔ Activa `anti-slop`
 │
 ├── 🛡️ "¿Quiero una auditoría defensiva de seguridad pre-launch / DevSecOps?"
 │    └── Ruta: PRE-LAUNCH SECURITY AUDIT ➔ Activa `security` (`security-and-hardening` + `security-auditor`)
 │
 ├── 🗺️ "¿Quiero diagramar mi arquitectura / mapa del sistema / secuencia de APIs / Mermaid a HTML?"
 │    └── Ruta: SYSTEM MAPPING & ARCHIFY ➔ Activa `archify`
 │
 ├── 🐛 "¿Tengo un error de código, compilación o despliegue?"
 │    └── Ruta: DEBUGGING & ERROR RECOVERY ➔ Activa `debugging-and-error-recovery` + `test-driven-development`
 │
 ├── 💡 "¿Tengo una idea / quiero validar un mercado?"
 │    └── Ruta: DISCOVERY ➔ Activa `interview-me` + `office-hours` + `startup-idea-validation`
 │
 ├── 💰 "¿Cómo cobro / cuánto cobrar / planes / Stripe?"
 │    └── Ruta: MONETIZATION ➔ Activa `saas-business-model` + `plan-ceo-review` + `pricing`
 │
 ├── ✂️ "¿Tengo demasiado alcance / cómo hago el MVP rápido?"
 │    └── Ruta: SCOPE-KILLER ➔ Activa `mvp-scope-killer`
 │
 ├── 🧠 "¿Cómo armo el sistema de IA / RAG / Prompts / Evals?"
 │    └── Ruta: AI-ARCH ➔ Activa `ai-product-architect` + `rag-implementation`
 │
 ├── 📐 "¿Cómo armo la arquitectura backend / frontend / DB?"
 │    └── Ruta: TECH-ARCH ➔ Activa `plan-eng-review` + `backend-architect` + `fastapi-pro` / `nextjs-app-router`
 │
 ├── 🏗️ "¿Quiero que construyas toda esta feature de punta a punta?"
 │    └── Ruta: FULL-BUILD ➔ Activa `autoplan` + `ralph-loop` + `test-driven-development`
 │
 ├── 🚀 "¿Cómo consigo usuarios / landing page / onboarding / SEO?"
 │    └── Ruta: GROWTH ➔ Activa `launch-growth-loop` + `saas-launch-revenue`
 │
 ├── 🧐 "¿Estoy seguro de esta decisión técnica difícil?"
 │    └── Ruta: ADVERSARIAL ➔ Activa `doubt-driven-development` + `founder-technical-decision`
 │
 └── 🎓 "¿Qué aprendimos / guarda este patrón para siempre?"
      └── Ruta: PERSISTENCE ➔ Activa `retro` + `self-learning-skills`
```

## Dónde vive cada skill

god-mode se instala en plugins separados. Si la skill de una ruta no está disponible en la sesión, no la simules: decile al usuario qué plugin instalar y seguí con lo que sí está disponible.

| Plugin | Contenido | Skills que usa este router |
| --- | --- | --- |
| `god-mode-core` | incluido siempre | `ai-product-architect`, `anti-slop`, `archify`, `debugging-and-error-recovery`, `doubt-driven-development`, `launch-growth-loop`, `mvp-scope-killer`, `saas-business-model`, `security`, `security-and-hardening`, `test-driven-development`, `thermo-nuclear-code-quality-review`, `thermo-nuclear-review`, `thermos` |
| `god-mode-dev` | arquitectura, backend, IA y planificación | `autoplan`, `backend-architect`, `fastapi-pro`, `founder-technical-decision`, `interview-me`, `nextjs-app-router`, `office-hours`, `plan-ceo-review`, `plan-eng-review`, `rag-implementation`, `ralph-loop`, `retro`, `self-learning-skills` |
| `god-mode-growth` | pricing, validación y crecimiento | `pricing`, `saas-launch-revenue`, `startup-idea-validation` |
