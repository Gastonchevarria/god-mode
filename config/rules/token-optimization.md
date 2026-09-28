# Token Optimization Protocol (Regla Global)

## Objetivo
Reducir el consumo de tokens sin sacrificar calidad. Esta regla aplica a todas las sesiones y nunca tiene prioridad sobre los Límites de autonomía.

## 1. Brevedad Obligatoria
- Respuestas cortas por defecto. No repitas lo que el usuario ya sabe.
- Nunca re-resumas artefactos ni archivos entregados: apuntá a ellos.
- Listas antes que párrafos cuando el contenido es paralelo.
- Sin preámbulos vacíos ni despedidas largas.

## 2. Context Hygiene
- No releas archivos que ya leíste en la sesión salvo que hayan cambiado.
- Si solo necesitás una sección, leé ese rango de líneas y no el archivo entero.
- Para encontrar algo concreto, usá la herramienta de búsqueda antes de abrir archivos.
- No abras más de 3 archivos por turno salvo que la tarea lo requiera.

## 3. Tool Call Discipline
- Si varias llamadas no dependen entre sí, hacelas juntas en un mismo mensaje.
- No corras el mismo comando dos veces salvo error o cambio.
- No vuelques archivos de más de 100 líneas completos a la conversación.

## 4. Output Frugality
- Limitá la salida de comandos con `| head -n 20` o `| tail -n 10`.
- Resumí los diffs en 2 o 3 bullets. Excepción: antes de una acción que requiere confirmación (push, deploy, borrados), mostrá el cambio completo o ofrecelo.
- No generes código de ejemplo si el usuario no lo pidió.

## 5. Auto-Compact Triggers
El agente debe recomendar compactar (en Claude Code, `/compact`) cuando detecte:
- Más de 30 tool calls en la conversación actual.
- Más de 15 mensajes de ida y vuelta.
- Un cambio de tema mayor.
- Relectura de archivos ya procesados.

Para decidir y compactar, usá la skill `auto-compact`.

## 6. Smart Skill Loading
- No releas el SKILL.md de una skill que ya cargaste en la sesión.
- Cargá un SKILL.md solo cuando la tarea lo requiere.
- No cargues más de 2 skills por turno, salvo con `/god` o `/autoplan`.
