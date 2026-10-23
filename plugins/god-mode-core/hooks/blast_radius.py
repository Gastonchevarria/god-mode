#!/usr/bin/env python3
"""PreToolUse hook: shows what a destructive action would touch, and blocks it so the user decides.

Two kinds of action, in a session whose project is the hook's cwd:

* Bash commands that throw work away: `rm` outside the temp directory, `git reset --hard`,
  `git checkout -- <paths>`, `git restore <paths>` (not `--staged`), `git clean -f`,
  `git stash drop|clear`, `git branch -D` and force pushes. Before blocking, the hook lists what
  the command would discard (uncommitted files, files under the rm targets, the branch).
  A `git reset --hard` on a clean tree discards nothing and passes.
* Writes (Write, Edit, MultiEdit, NotebookEdit) outside the project: anything not under cwd,
  the temp directory or ~/.claude. Work for another project belongs in a session opened there.

The hook exits 2 with the reason, so Claude stops and asks the user instead of running it.
GOD_MODE_BLAST=off turns it off. Any error inside the hook lets the action through.
"""
import json
import os
import shlex
import subprocess
import sys
import tempfile

WRITE_TOOLS = {"Write": "file_path", "Edit": "file_path", "MultiEdit": "file_path", "NotebookEdit": "notebook_path"}
MAX_LISTED = 12


def real(path):
    return os.path.realpath(os.path.expanduser(path))


def temp_roots():
    roots = {real(tempfile.gettempdir()), "/tmp", "/private/tmp"}
    for var in ("TMPDIR", "TMP", "TEMP"):
        if os.environ.get(var):
            roots.add(real(os.environ[var]))
    return roots


def under(path, root):
    path, root = real(path), real(root)
    return path == root or path.startswith(root.rstrip("/") + "/")


def listing(items, unit="archivos"):
    shown = ", ".join(items[:MAX_LISTED]) + (", ..." if len(items) > MAX_LISTED else "")
    return f"{len(items)} {unit}: {shown}" if items else f"0 {unit}"


def uncommitted(cwd):
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=cwd,
                             capture_output=True, text=True, timeout=10, check=False).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [line[3:].strip() for line in out.splitlines() if line.strip()]


def current_branch(cwd):
    try:
        out = subprocess.run(["git", "branch", "--show-current"], cwd=cwd, capture_output=True, text=True,
                             timeout=10, check=False).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
    return out


def files_under(paths, cwd):
    found = []
    for p in paths:
        full = p if os.path.isabs(p) else os.path.join(cwd, p)
        if os.path.isdir(full) and not os.path.islink(full):
            for root, _dirs, files in os.walk(full):
                found += [os.path.relpath(os.path.join(root, f), cwd) for f in files]
                if len(found) > 500:
                    return found
        elif os.path.lexists(full):
            found.append(os.path.relpath(full, cwd))
    return found


def segments(command):
    """Each simple command of a shell line as a list of words (pipes, ;, && and || split them)."""
    try:
        words = shlex.split(command)
    except ValueError:
        words = command.split()
    out, cur = [], []
    for w in words:
        if w in ("|", "||", "&&", ";", "&"):
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append(w)
    if cur:
        out.append(cur)
    return out


def check_bash(command, cwd):
    """Returns the reason to block, or None."""
    for words in segments(command):
        if not words:
            continue
        head = words[0]
        if head == "rm":
            targets = [w for w in words[1:] if not w.startswith("-")]
            outside = [t for t in targets if not any(under(t if os.path.isabs(t) else os.path.join(cwd, t), r)
                                                     for r in temp_roots())]
            if outside:
                return (f"Blast radius: `rm` borraría {listing(files_under(outside, cwd))}. Nada se borra sin el OK "
                        f"del usuario: proponé mover a _to_delete/ (mkdir -p _to_delete && mv ... _to_delete/) "
                        f"o pedile que lo borre él.")
        if head != "git" or len(words) < 2:
            continue
        sub, rest = words[1], words[2:]
        if sub == "reset" and "--hard" in rest:
            changes = uncommitted(cwd)
            if changes:
                return (f"Blast radius: `git reset --hard` descartaría {listing(changes)} sin commitear. "
                        f"Pedile al usuario que confirme, o guardalos antes con git stash push -m \"...\".")
        elif sub == "checkout" and "--" in rest:
            changes = uncommitted(cwd)
            if changes:
                return (f"Blast radius: `git checkout -- ...` descartaría cambios de {listing(changes)}. "
                        f"Pedile al usuario que confirme, o guardalos antes con git stash.")
        elif sub == "restore" and "--staged" not in rest and any(not w.startswith("-") for w in rest):
            changes = uncommitted(cwd)
            if changes:
                return (f"Blast radius: `git restore` descartaría cambios de {listing(changes)}. "
                        f"Pedile al usuario que confirme, o guardalos antes con git stash.")
        elif sub == "clean" and any(w.startswith("-") and "f" in w for w in rest):
            changes = uncommitted(cwd)
            return (f"Blast radius: `git clean -f` borraría archivos sin trackear ({listing(changes)} sin commitear "
                    f"en el árbol). Pedile al usuario que confirme.")
        elif sub == "stash" and rest and rest[0] in ("drop", "clear"):
            return "Blast radius: `git stash " + rest[0] + "` borra trabajo guardado. Pedile al usuario que confirme."
        elif sub == "branch" and "-D" in rest:
            return f"Blast radius: `git branch -D` borra una rama sin merge ({' '.join(rest)}). Pedile al usuario que confirme."
        elif sub == "push" and ("--force" in rest or "-f" in rest or "--force-with-lease" in rest
                                or any(w.startswith("+") for w in rest)):
            return (f"Blast radius: push forzado sobre `{current_branch(cwd) or 'la rama actual'}` reescribe el "
                    f"historial remoto. Pedile al usuario que confirme.")
    return None


def check_write(path, cwd):
    """Returns the reason to block, or None."""
    full = path if os.path.isabs(path) else os.path.join(cwd, path)
    allowed = [cwd, os.path.expanduser("~/.claude"), *temp_roots()]
    if path == "/dev/null" or any(under(full, root) for root in allowed):
        return None
    return (f"Cerca de escritura: `{path}` queda fuera de este proyecto ({cwd}). Si es de otro proyecto, "
            f"abrí una sesión ahí; si de verdad va acá, pedile al usuario que lo confirme.")


def main():
    if os.environ.get("GOD_MODE_BLAST", "").lower() == "off":
        return 0
    try:
        data = json.load(sys.stdin)
        tool = data.get("tool_name", "")
        cwd = real(data.get("cwd") or os.getcwd())
        tool_input = data.get("tool_input") or {}
        reason = None
        if tool == "Bash":
            reason = check_bash(str(tool_input.get("command", "")), cwd)
        elif tool in WRITE_TOOLS:
            path = str(tool_input.get(WRITE_TOOLS[tool], "") or "")
            if path:
                reason = check_write(path, cwd)
        if not reason:
            return 0
        print(reason, file=sys.stderr)
        return 2
    except Exception:  # noqa: BLE001 - a broken hook must never block an action
        return 0


if __name__ == "__main__":
    sys.exit(main())
