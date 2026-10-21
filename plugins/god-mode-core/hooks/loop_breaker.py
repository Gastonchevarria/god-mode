#!/usr/bin/env python3
"""PreToolUse hook for Bash: stops a command that keeps being retried.

A workflow that retries the same failing command "until it works" can run for hours and
burn the whole budget. Claude Code runs this hook before each Bash command; when the same
command is about to run for the fourth time in a row (GOD_MODE_LOOP_MAX, default 3,
changes the limit; 0 turns the hook off), the hook blocks it and tells Claude to stop,
report the error and wait for the user. Running any other command resets the count.
A `sleep` before the retry does not hide the loop. Counts are kept per session in the
temp directory. Any error inside the hook lets the command through: the hook never
blocks by accident.
"""
import json
import os
import re
import sys
import tempfile

SLEEP_PREFIX = re.compile(r"^(?:sleep\s+[\d.]+[smh]?\s*(?:;|&&)\s*)+")


def normalize(command):
    command = SLEEP_PREFIX.sub("", command.strip())
    return " ".join(command.split())


def state_path(session_id):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id or "default")[:80]
    return os.path.join(tempfile.gettempdir(), f"god-mode-loop-{safe}.json")


def main():
    try:
        limit = int(os.environ.get("GOD_MODE_LOOP_MAX", "3"))
    except ValueError:
        limit = 3
    if limit <= 0:
        return 0
    try:
        data = json.load(sys.stdin)
        if data.get("tool_name") != "Bash":
            return 0
        command = normalize(str((data.get("tool_input") or {}).get("command", "")))
        if not command:
            return 0
        path = state_path(str(data.get("session_id", "")))
        try:
            with open(path, encoding="utf-8") as f:
                state = json.load(f)
        except (OSError, ValueError):
            state = {}
        count = state.get("count", 0) + 1 if state.get("last") == command else 1
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"last": command, "count": count}, f)
        if count <= limit:
            return 0
        shown = command if len(command) <= 120 else command[:117] + "..."
        print(f"god-mode: `{shown}` ya corrió {limit} veces seguidas. No lo reintentes: pará acá, "
              "dejá el error tal cual en el informe y preguntale al usuario cómo seguir.", file=sys.stderr)
        return 2
    except Exception:  # noqa: BLE001 - a broken hook must never block a command
        return 0


if __name__ == "__main__":
    sys.exit(main())
