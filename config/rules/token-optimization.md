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
- Si el proyecto tiene `graphify-out/graph.json`, preguntá primero al grafo (`graphify query`, `path`, `explain`) antes de un grep amplio o de leer muchos archivos.

## 3. Tool Call Discipline
- Si varias llamadas no dependen entre sí, hacelas juntas en un mismo mensaje.
- No corras el mismo comando dos veces salvo error o cambio.

## 4. Output Frugality
- Recortá la salida larga de comandos que funcionaron (`head`, `tail`, `grep`). Si un comando o un test falló, leé el error completo.
- Resumí los diffs en 2 o 3 bullets. Excepción: antes de una acción de los Límites de autonomía, o cuando el usuario pide ver el cambio, mostralo completo.
- No generes código de ejemplo si el usuario no lo pidió.

## 5. Compactación
- En Claude Code la sesión compacta sola al llenar `autoCompactWindow` (lo pone `god-mode doctor --fix`). Cada llamada reenvía todo el contexto, así que una sesión más grande cuesta más en cada paso.
- Recomendá `/compact` antes de eso cuando la sesión arrastra contexto que ya no sirve: salidas largas, archivos ya procesados o un tramo de trabajo cerrado.
- Si el usuario cambia de tema, recomendá `/clear` o una sesión nueva: el contexto anterior ya no sirve y compactarlo igual se paga.

Para decidir y compactar, usá la skill `auto-compact`.

## 6. Smart Skill Loading
- No releas el SKILL.md de una skill que ya cargaste en la sesión.
- Cargá un SKILL.md solo cuando la tarea lo requiere.
