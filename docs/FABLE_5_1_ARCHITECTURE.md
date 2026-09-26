# Fable 5.1 Architecture & Frontier Prompt Engineering Guide

## 1. El Salto Evolutivo a "Fable 5.1"
La integración de las técnicas extraídas de los leaks de modelos de frontera (Anthropic Claude Fable 5.1, OpenAI GPT-5 Thinking, Cursor IDE y Google DeepMind Antigravity) transforma a nuestro agente de un asistente pasivo a un **Súper Agente Autónomo de Ejecución Ininterrumpida**.

---

## 2. Los 4 Pilares Fundamentales Implementados

### Pilar 1: The "Never Stop Short" Mandate (Anthropic / Claude Code)
- **Eliminación del Cansancio del Modelo**: Los LLMs convencionales tienden a detenerse tras 2 o 3 pasos y devolver el control al usuario con sugerencias vagas ("Ahora puedes agregar X").
- **Mecanismo de Auto-Inspección (Final Paragraph Check)**: El agente audita el último párrafo de su borrador. Si contiene promesas no cumplidas ("A continuación voy a crear el test..."), el turno se detiene internamente y el agente ejecuta las herramientas necesarias antes de responder.

### Pilar 2: Report Outcomes, Not Intentions (Anti-Racionalización)
- **Cero Auto-Engaño**: Se prohíbe asumir que un comando funcionó solo porque se envió. Toda afirmación debe estar respaldada por el resultado observable de una tool (`exit code 0`, archivos modificados comprobados).
- **Fallas en la Primera Línea**: Cualquier error o comportamiento anómalo se comunica de inmediato, sin enmascararlo ni minimizarlo.

### Pilar 3: Look Before You Assert & Cero Thinking in Comments (Cursor IDE)
- **Inspección Previa Obligatoria**: Antes de proponer cambios en un archivo o API, el agente debe leer el código circundante y los tipos existentes.
- **Limpieza de Código**: Los comentarios de código nunca se usan para monólogos internos. Solo se comenta lógica no trivial o restricciones de arquitectura.

### Pilar 4: Imperativo Estético y Anti-Genérico (Google Antigravity)
- **Diseño de Clase Mundial**: El agente tiene estrictamente prohibido generar interfaces genéricas con colores primarios planos (#0000FF) o plantillas aburridas. Todo desarrollo UI debe incluir paletas HSL afinadas, microinteracciones y elevación sutil en dark mode.

---

## 3. Estado de Activación en el Ecosistema GOD
- **Ruta Activa**: Todas las 12 rutas del `startup-god-router` ahora heredan y aplican estos principios automáticamente.
- **Global**: Disponible en todos los proyectos y repositorios de Antigravity.
