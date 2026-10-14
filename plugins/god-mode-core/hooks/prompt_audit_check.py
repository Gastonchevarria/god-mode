#!/usr/bin/env python3
"""
SessionStart hook for compactions: asks Claude to run Claude Code's prompt-audit on the
instruction files that changed since the last audit of this project.

Claude Code sends the hook input as JSON on stdin (`source`, `model`, `cwd`, `session_id`).
The script prints context for Claude, or nothing when there is nothing to audit.

GOD_MODE_PROMPT_AUDIT chooses when:
  changed  (default) after a compaction, only the files that changed since the last audit
  always   after every compaction, every covered file
  off      never
GOD_MODE_PROMPT_AUDIT_MAX_KB caps what runs on its own (default 60, 0 = no cap). Above the cap,
Claude only offers the audit to the user.

Covered files: CLAUDE.md, CLAUDE.local.md and AGENTS.md in the project, its parents and its
subfolders, and the rules, commands, subagents, output styles and skills under the project's
.claude/ and ~/.claude/. Linked skill folders (god-mode's own skills) are left out: they are
audited in their own repository. Changes are detected by size and modification time.
"""

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
DEFAULT_MAX_KB = 60
LISTED_FILES = 15


def claude_dir_files(base):
    files = [base / "CLAUDE.md", base / "AGENTS.md"]
    for sub in CLAUDE_SUBDIRS:
        folder = base / sub
        if folder.is_dir():
            files += sorted(folder.rglob("*.md"))
    skills = base / "skills"
    if skills.is_dir():
        files += sorted(entry / "SKILL.md" for entry in skills.iterdir() if not entry.is_symlink())
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


def snapshot(files):
    rows = {}
    for path in files:
        try:
            if path.is_file():
                st = path.stat()
                rows[str(path)] = [st.st_size, st.st_mtime_ns]
        except OSError:
            continue
    return rows


def model_name(model):
    if isinstance(model, dict):
        model = model.get("id") or model.get("display_name")
    return model if isinstance(model, str) and model else None


def max_bytes():
    try:
        return int(float(os.environ.get("GOD_MODE_PROMPT_AUDIT_MAX_KB", DEFAULT_MAX_KB)) * 1024)
    except ValueError:
        return DEFAULT_MAX_KB * 1024


def display(path, project, home):
    p = Path(path)
    for base, prefix in ((project, ""), (home, "~/")):
        try:
            return prefix + str(p.relative_to(base))
        except ValueError:
            continue
    return path


def file_list(paths, project, home):
    lines = [f"- {display(p, project, home)}" for p in paths[:LISTED_FILES]]
    if len(paths) > LISTED_FILES:
        lines.append(f"- y {len(paths) - LISTED_FILES} más")
    return "\n".join(lines)


def message(changed, size, model, first_time, project, home, cap):
    count = f"{len(changed)} archivo{'' if len(changed) == 1 else 's'}"
    kb = max(1, round(size / 1024))
    why = "Es el primer audit de este proyecto." if first_time else "Cambiaron instrucciones desde el último audit."
    files = file_list(changed, project, home)
    if cap and size > cap:
        return f"""# god-mode: instrucciones nuevas o cambiadas

{why} Son {count} ({kb} KB), más que el tope del audit automático ({cap // 1024} KB), así que no corre solo:
{files}

Seguí con lo pendiente. Al final de tu próxima respuesta, ofrecé en una línea auditarlos con `/god` (ruta CONTEXT-HEALTH). No lo lances sin el "sí" del usuario.
"""
    target = f"`{model}`" if model else "el modelo de esta sesión"
    return f"""# god-mode: audit de instrucciones después de compactar

{why} Entran en el audit {count} ({kb} KB):
{files}

Antes de seguir con lo pendiente:
1. Si la skill `claude-api` no está entre tus skills (en Cowork viene desactivada), decilo en una línea y seguí con lo pendiente.
2. Lanzá un subagente con `model: "sonnet"`. Pedile que cargue la skill `claude-api` con el argumento `prompt-audit`, que audite solo los archivos de arriba con {target} como modelo destino, que no edite ningún archivo y que te devuelva el reporte y el diff propuesto.
3. Contale al usuario en 3 a 5 líneas cuántos hallazgos hubo y los de mayor impacto, con archivo y línea. Ofrecé aplicar el diff, sin aplicarlo: cambiar instrucciones necesita su "sí". Los archivos de `~/.claude` afectan a todos sus proyectos.
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
        current = snapshot(instruction_files(project, home))
        previous = (state.get("projects") or {}).get(str(project))
        # Entries written before 1.10.0 only kept a hash: take today's files as the baseline.
        migrated = previous is not None and not isinstance(previous.get("files"), dict)
        known = (previous or {}).get("files") if not migrated else current
        known = known if isinstance(known, dict) else {}
        if mode == "always":
            changed = sorted(current)
        else:
            changed = sorted(p for p, sig in current.items() if known.get(p) != sig)
        state.setdefault("projects", {})[str(project)] = {"files": current, "at": now}
        state["last"] = {"session_id": data.get("session_id"), "at": now}
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=1), encoding="utf-8")
        os.replace(tmp, state_path)

    if not changed:
        return 0
    size = sum(current[p][0] for p in changed)
    print(message(changed, size, model_name(data.get("model")), previous is None, project, home, max_bytes()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
