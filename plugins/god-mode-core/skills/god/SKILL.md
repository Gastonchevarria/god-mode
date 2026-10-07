---
name: god
description: "Routes a request to the right god-mode skills and subagents and runs it end to end under the Fable 5.1 Protocol. Use when the user types /god or asks for 'full autonomous mode' or 'handle this end to end'. Not for ordinary single-skill requests; use that skill directly."
---

# DEV GOD-MODE Router

`/god` lee el pedido, elige una ruta y lo ejecuta de punta a punta. Cada ruta carga **una sola skill**, la que sirve para ese pedido; los pedidos de todos los días no cargan ninguna.

## Protocolo Fable 5.1

El protocolo ya está cargado en la sesión: lo ponen el bloque god-mode de `CLAUDE.md`, las reglas de Antigravity o el hook del plugin. No lo releas. Solo si en tu contexto no aparece la sección "Límites de autonomía", leé [`references/protocol.md`](references/protocol.md).

Los **Límites de autonomía** tienen prioridad sobre cualquier otra regla: push, deploys, borrados, migraciones, dinero o credenciales, mensajes a terceros e instalaciones externas requieren un "sí" explícito del usuario.

## Primera línea, siempre

Tu respuesta empieza con esta línea, antes de cualquier herramienta, incluida la carga de una skill:

```markdown
⚡ **GOD** · Ruta: [ruta] · Skills: [la skill, o "ninguna"] · [qué vas a hacer, en una frase]
```

Una sola línea: el diagnóstico largo va solo si el usuario lo pide.

## Cómo elegir

1. **Una ruta.** La más específica que encaje con el pedido.
2. **Si ninguna encaja claramente, la ruta es DIRECTA:** hacés el pedido vos, sin cargar skills. Es lo normal para un cambio chico, un refactor puntual, una pregunta, explicar código, un comando, configuración o un mensaje de commit. Nunca uses una ruta pesada (FULL-BUILD, `autoplan`) para un pedido chico.
3. **Una skill.** Cargá la que la ruta indica para ese caso. Otra skill entra solo cuando un paso posterior la necesita, nunca al principio "por las dudas".
4. **Skills que corren aparte.** Si la skill tiene `context: fork` (las de diseño), no ve la conversación: pasale en los argumentos el pedido completo y las rutas de los archivos.
5. **`/god` sin pedido.** Respondé con cuatro o cinco ejemplos de lo que puede hacer y preguntá qué necesita.

## Matriz de rutas

```text
[Pedido del usuario]
 ├── ⚡ Un cambio chico, una pregunta, explicar código, un comando, un commit, configuración
 │    └── Ruta: DIRECTA ➔ Activa ninguna skill: hacelo vos, con el protocolo
 │
 ├── 🐛 Un error de código, de build o de despliegue
 │    └── Ruta: DEBUGGING ➔ Activa `debugging-and-error-recovery`
 │         Después del fix, un test de regresión con `test-driven-development` si el proyecto tiene tests.
 │
 ├── 💥 Auditar un branch o un PR antes de mergear
 │    └── Ruta: THERMO-NUCLEAR REVIEW ➔ Activa `thermos` (lanza solo sus dos subagentes de revisión)
 │
 ├── 🧹 Limpiar código vago o anti-patrones de IA en TypeScript o JavaScript
 │    └── Ruta: ANTI-SLOP ➔ Activa `anti-slop`
 │
 ├── 🛡️ Seguridad
 │    └── Ruta: SECURITY ➔ Activa una:
 │         · auditar toda la app antes de lanzar ➔ `security`
 │         · asegurar una feature mientras se construye (login, uploads, webhooks) ➔ `security-and-hardening`
 │
 ├── 🗺️ Diagramar la arquitectura, un flujo o una secuencia de APIs
 │    └── Ruta: ARCHIFY ➔ Activa `archify`
 │
 ├── 💡 Una idea de producto
 │    └── Ruta: DISCOVERY ➔ Activa una:
 │         · la idea es vaga y falta saber qué quiere el usuario ➔ `interview-me`
 │         · ¿vale la pena construirla? veredicto seguir, pivotear o matar ➔ `office-hours`
 │         · mapear mercado, competidores, ICP y experimentos ➔ `startup-idea-validation`
 │
 ├── 💰 Cobrar
 │    └── Ruta: MONETIZATION ➔ Activa una:
 │         · modelo de cobro: por usuario, por uso, tiers ➔ `saas-business-model`
 │         · precios concretos o la página de precios ➔ `pricing`
 │         · el código de cobro con Stripe o Mercado Pago ➔ `saas-launch-revenue`
 │
 ├── ✂️ Demasiado alcance para un MVP
 │    └── Ruta: SCOPE-KILLER ➔ Activa `mvp-scope-killer`
 │
 ├── 🧠 Un sistema de IA: LLMs, RAG, prompts, evals
 │    └── Ruta: AI-ARCH ➔ Activa una:
 │         · arquitectura: modelos, costos, guardrails, evals ➔ `ai-product-architect`
 │         · implementar el RAG: chunking, embeddings, retrieval ➔ `rag-implementation`
 │
 ├── 📐 Arquitectura técnica
 │    └── Ruta: TECH-ARCH ➔ Activa una:
 │         · diseñar el backend o la base de datos ➔ `backend-architect`
 │         · revisar un plan técnico que ya existe ➔ `plan-eng-review`
 │         · estructurar una app Next.js ➔ `nextjs-app-router`
 │         · estructurar una API en FastAPI ➔ `fastapi-pro`
 │
 ├── 🏗️ Construir una feature de punta a punta
 │    └── Ruta: FULL-BUILD ➔ Activa una:
 │         · feature clara, de varios archivos ➔ `incremental-implementation`, con tests en cada paso
 │         · feature grande o poco definida ➔ `autoplan` primero; después ejecutá el plan paso a paso
 │         `ralph-loop` solo si el usuario pide un loop autónomo largo.
 │
 ├── 🚀 Conseguir usuarios
 │    └── Ruta: GROWTH ➔ Activa una:
 │         · landing, activación, onboarding o referidos dentro del producto ➔ `launch-growth-loop`
 │         · lanzamiento, canales, Product Hunt ➔ `launch`
 │         · posicionamiento en Google ➔ `seo-audit`
 │
 ├── 🧐 Cuestionar una decisión técnica difícil
 │    └── Ruta: ADVERSARIAL ➔ Activa una:
 │         · poner a prueba una decisión o un cambio antes de cerrarlo ➔ `doubt-driven-development`
 │         · dejar registrada una decisión de una sola vía (ADR) ➔ `founder-technical-decision`
 │
 ├── 🎓 Aprender de lo hecho
 │    └── Ruta: PERSISTENCE ➔ Activa una:
 │         · retrospectiva de un sprint, una feature o un incidente ➔ `retro`
 │         · guardar un procedimiento o un patrón para reusarlo ➔ `self-learning-skills`
 │
 ├── 💾 La sesión está pesada o se acaban los tokens
 │    └── Ruta: CONTEXT-HEALTH ➔ Activa una:
 │         · compactar la sesión ➔ `auto-compact`
 │         · configurar reglas y contexto del proyecto ➔ `context-engineering`
 │
 └── 🎨 UI que se sienta nativa, pixel-perfect, animaciones o verificar estados
      └── Ruta: DESIGN ➔ Activa una:
           · construir un componente o pantalla desde un mockup, una captura o una descripción ➔ `design-to-web`
           · decidir cómo se tiene que sentir el movimiento, timing o coreografía ➔ `motion-direction`
           · agregar o arreglar animaciones en el código ➔ `motion-design`
           · verificar estados, accesibilidad o fidelidad en el navegador ➔ `ui-states-verification`
           Un cambio puntual de estilo, como un color o un margen, es DIRECTA.
```

## Dónde vive cada skill

god-mode se instala en plugins separados. Si la skill de una ruta no está disponible en la sesión, no la simules: decile al usuario qué plugin instalar y seguí con lo que sí está disponible.

| Plugin | Contenido | Skills que usa este router |
| --- | --- | --- |
| `god-mode-core` | incluido siempre | `ai-product-architect`, `anti-slop`, `archify`, `auto-compact`, `context-engineering`, `debugging-and-error-recovery`, `doubt-driven-development`, `launch-growth-loop`, `mvp-scope-killer`, `saas-business-model`, `security`, `security-and-hardening`, `test-driven-development`, `thermos` |
| `god-mode-dev` | arquitectura, backend, IA y planificación | `autoplan`, `backend-architect`, `fastapi-pro`, `founder-technical-decision`, `incremental-implementation`, `interview-me`, `nextjs-app-router`, `office-hours`, `plan-eng-review`, `rag-implementation`, `ralph-loop`, `retro`, `self-learning-skills` |
| `god-mode-growth` | pricing, validación y crecimiento | `launch`, `pricing`, `saas-launch-revenue`, `seo-audit`, `startup-idea-validation` |
| `god-mode-design` | UI pulida: tokens, estados, motion y verificación | `design-to-web`, `motion-design`, `motion-direction`, `ui-states-verification` |
