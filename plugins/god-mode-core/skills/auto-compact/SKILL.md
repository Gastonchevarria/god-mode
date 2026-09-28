---
name: auto-compact
description: "Detects context bloat in a long session and proposes compacting it with a structured summary before quality drops. Use when the user says 'the session feels heavy', 'compact', 'I'm running out of tokens' or 'start fresh', or after 30+ tool calls or a major topic change."
---

# Auto-Compact

Keeps long sessions fast and accurate. Watches for context bloat, tells the user in one line, and compacts with a summary that preserves everything needed to continue.

## Señales de bloat

| Nivel | Señales | Acción |
| --- | --- | --- |
| 🟢 Sana | Menos de 15 tool calls, un solo tema, ningún archivo releído | Seguir normal |
| 🟡 Pesada | 15 a 30 tool calls, o 10 a 15 mensajes de ida y vuelta, o un archivo grande leído entero, o salidas largas de comandos | Mencionarlo en una línea al terminar la respuesta actual |
| 🔴 Saturada | Más de 30 tool calls, o más de 15 mensajes, o un cambio de tema mayor, o releer archivos ya procesados, o respuestas que olvidan decisiones anteriores | Proponer compactar antes de seguir |

Contá solo lo observable en la conversación. Nunca inventes porcentajes de contexto usado.

## Protocolo de compactación

1. **Detectar.** Evaluá las señales al terminar cada tarea, no en medio de una.
2. **Notificar.** Una sola línea, sin interrumpir el trabajo en curso:
   `🔴 La sesión está saturada (N tool calls, cambio de tema). ¿Compacto con un resumen antes de seguir?`
3. **Compactar**, solo con el "sí" del usuario:
   - Escribí el resumen estructurado de abajo.
   - En Claude Code, pedile al usuario que corra `/compact` pegando ese resumen como instrucción (`/compact <resumen>`), o que abra una sesión nueva con `/clear` y el resumen.
   - En Cowork, la compactación es automática: ofrecé seguir en una tarea nueva que arranque con el resumen.
4. **Verificar.** Después de compactar, confirmá en una línea el objetivo y el próximo paso según el resumen.

### Resumen estructurado

```markdown
## Estado de la sesión
- **Objetivo:** qué se está construyendo o resolviendo, en una frase.
- **Decisiones tomadas:** cada decisión con su motivo, una por línea.
- **Hecho:** qué quedó terminado y verificado (tests, commits, archivos).
- **Pendiente:** próximos pasos en orden.
- **Archivos clave:** rutas que hay que volver a mirar, con una línea de por qué.
- **No repetir:** caminos que ya se probaron y fallaron.
```

Nada de lo que está en "Decisiones tomadas" o "No repetir" puede quedar afuera del resumen: es lo que más cuesta reconstruir.

## Métricas de salud del contexto

| Métrica | 🟢 | 🟡 | 🔴 |
| --- | --- | --- | --- |
| Tool calls en la conversación | 0–15 | 16–30 | más de 30 |
| Mensajes de ida y vuelta | 0–10 | 11–15 | más de 15 |
| Archivos releídos sin cambios | 0 | 1 | 2 o más |
| Temas distintos | 1 | 2 | 3 o más |
| Salidas de comandos de más de 100 líneas | 0 | 1–2 | 3 o más |

El nivel de la sesión es el peor de sus métricas.

## Prevención

- Leé solo la parte del archivo que necesitás (por rango de líneas) y buscá con la herramienta de búsqueda antes de abrir archivos enteros.
- Recortá salidas largas con `head` o `tail`.
- Agrupá en un solo mensaje las llamadas que no dependen entre sí.
- No releas un archivo que no cambió.

## Integración con /god

`/god` enruta a esta skill en la ruta **CONTEXT-HEALTH**, junto con `context-engineering`, cuando el usuario dice que la sesión está pesada, que se le acaban los tokens o que compacte. `context-engineering` se ocupa de preparar bien el contexto de la sesión siguiente (reglas del proyecto, archivos a cargar); esta skill decide cuándo compactar y qué conservar.
