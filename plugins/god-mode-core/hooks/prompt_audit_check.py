#!/usr/bin/env python3
"""
SessionStart hook for compactions: asks Claude to run Claude Code's prompt-audit when the
instructions that load in this project changed since the last audit.

Claude Code sends the hook input as JSON on stdin (`source`, `model`, `cwd`, `session_id`).
The script prints context for Claude, or nothing when there is nothing to audit.

GOD_MODE_PROMPT_AUDIT chooses when:
  changed  (default) after a compaction, only if the instructions changed since the last audit
  always   after every compaction
  off      never

The fingerprint covers the files prompt-audit reads: CLAUDE.md, CLAUDE.local.md and AGENTS.md
in the project, its parents and its subfolders, and the rules, skills, commands, subagents and
output styles under the project's .claude/ and ~/.claude/. It uses each file's size and
modification time, never its content.
"""

import hashlib
import json
import os
import sys
import time
from pathlib import Path

try:
    import fcntl
except ImportError:  # Windows: no lock, the session dedupe below still applies
    fcntl = None

INSTRUCTION_FILES = ("CLAUDE.md", "CLAUDE.local.md", "AGENTS.md")
CLAUDE_SUBDIRS = ("rules", "commands", "agents", "output-styles")
SKIP_DIRS = {"node_modules", "__pycache__", "venv", "dist", "build", "target", "vendor", "coverage"}
MAX_DIRS = 4000
SAME_COMPACTION_SECONDS = 60
MODEL_ALIASES = ("fable", "opus", "sonnet", "haiku")


def claude_dir_files(base):
    files = [base / "CLAUDE.md", base / "AGENTS.md"]
    for sub in CLAUDE_SUBDIRS:
        folder = base / sub
        if folder.is_dir():
            files += sorted(folder.rglob("*.md"))
    skills = base / "skills"
    if skills.is_dir():
        files += sorted(entry / "SKILL.md" for entry in skills.iterdir())
    return files


def instruction_files(project, home):
    files = [folder / name for folder in (project, *project.parents) for name in INSTRUCTION_FILES]
    for walked, (dirpath, dirnames, filenames) in enumerate(os.walk(project)):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS)
        if walked >= MAX_DIRS:
            break
        if Path(dirpath) != project:
            files += [Path(dirpath) / name for name in INSTRUCTION_FILES if name in filenames]
    files += claude_dir_files(project / ".claude")
    if (home / ".claude") != (project / ".claude"):
        files += claude_dir_files(home / ".claude")
    return files


def fingerprint(files):
    rows = set()
    for path in files:
        try:
            st = path.stat()
        except OSError:
            continue
        rows.add(f"{path}\0{st.st_size}\0{st.st_mtime_ns}")
    return hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest(), len(rows)


def message(model, files_count, first_time):
    name = model if isinstance(model, str) else json.dumps(model or "")
    alias = next((a for a in MODEL_ALIASES if a in name.lower()), None)
    model_hint = (f'con `model: "{alias}"`, el mismo modelo de esta sesión,' if alias
                  else "con el mismo modelo de esta sesión si el Agent tool lo permite,")
    why = ("Es el primer audit de este proyecto." if first_time else
           "Las instrucciones que se cargan en este proyecto cambiaron desde el último audit.")
    return f"""# god-mode: audit de instrucciones después de compactar

{why} Entran en el audit {files_count} archivos: CLAUDE.md, AGENTS.md, reglas, skills, comandos, subagentes y estilos.

Antes de seguir con lo pendiente:
1. Si la skill `claude-api` no está entre tus skills (en Cowork viene desactivada), decilo en una línea y seguí con lo pendiente.
2. Lanzá un subagente {model_hint} para que el audit apunte a ese modelo. Pedile que cargue la skill `claude-api` con el argumento exacto `prompt-audit`, sin nada más, así usa el alcance por defecto. Que no edite ningún archivo y te devuelva el reporte y el diff propuesto.
3. Contale al usuario en 3 a 5 líneas cuántos hallazgos hubo y los de mayor impacto, con archivo y línea. Ofrecé aplicar el diff, sin aplicarlo: cambiar instrucciones necesita su "sí". Los archivos de `~/.claude` afectan a todos sus proyectos. Las skills de god-mode se cambian en el repo god-mode, no a través de los links de `~/.claude/skills`.
"""


def main():
    mode = os.environ.get("GOD_MODE_PROMPT_AUDIT", "changed").strip().lower()
    if mode == "off":
        return 0
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if data.get("source") != "compact":
        return 0
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()).resolve()
    home = Path.home()
    state_path = home / ".claude" / ".god-mode-prompt-audit.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)

    with open(state_path.with_suffix(".lock"), "w", encoding="utf-8") as lock:
        if fcntl:
            fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            state = {}
        now = time.time()
        last = state.get("last") or {}
        if last.get("session_id") == data.get("session_id") and now - last.get("at", 0) < SAME_COMPACTION_SECONDS:
            return 0
        digest, count = fingerprint(instruction_files(project, home))
        previous = (state.get("projects") or {}).get(str(project))
        if mode != "always" and previous and previous.get("fingerprint") == digest:
            return 0
        state.setdefault("projects", {})[str(project)] = {"fingerprint": digest, "files": count, "at": now}
        state["last"] = {"session_id": data.get("session_id"), "at": now}
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
        os.replace(tmp, state_path)

    print(message(data.get("model"), count, previous is None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
