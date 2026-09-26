#!/usr/bin/env bash
# End-to-end checks for install.sh and bin/god-mode using a throwaway HOME.
# Usage: bash tests/smoke.sh
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0

check() {
    local desc="$1"; shift
    if "$@"; then
        PASS=$((PASS + 1)); echo "  ok   $desc"
    else
        FAIL=$((FAIL + 1)); echo "  FAIL $desc"
    fi
}

count_links() { find "$1" -maxdepth 1 -type l 2>/dev/null | wc -l | tr -d ' '; }
pack_size() { python3 -c "import json,sys;print(len(json.load(open('$REPO/config/packs.json'))['packs'][sys.argv[1]]))" "$1"; }
total_skills() { find "$REPO" -path "*/skills/*/SKILL.md" -not -path "*/references/*" | awk -F/ '{print $(NF-1)}' | sort -u | wc -l | tr -d ' '; }

fresh_home() {
    export HOME="$WORK/home-$1"
    rm -rf "$HOME"; mkdir -p "$HOME"
}

run_install() { (cd "$WORK" && bash "$REPO/install.sh" "$@" >"$WORK/install.log" 2>&1); }
cli() { python3 "$HOME/.local/bin/god-mode" "$@"; }

echo "== Instalación limpia sin Antigravity"
fresh_home plain
check "install.sh termina con código 0" run_install --pack=all
check "no crea ~/.gemini si Antigravity no está instalado" test ! -e "$HOME/.gemini"
check "no escribe .cursorrules ni AGENTS.md en la carpeta actual" test ! -e "$WORK/.cursorrules" -a ! -e "$WORK/AGENTS.md"
check "enlaza todas las skills en ~/.claude/skills" test "$(count_links "$HOME/.claude/skills")" = "$(total_skills)"
check "instala los 6 subagentes" test "$(find "$HOME/.claude/agents" -name '*.md' | wc -l | tr -d ' ')" = 6
check "CLAUDE.md tiene el bloque gestionado una sola vez" test "$(grep -c 'god-mode:start' "$HOME/.claude/CLAUDE.md")" = 1
check "CLAUDE.md incluye los límites de autonomía" grep -q "Límites de autonomía" "$HOME/.claude/CLAUDE.md"

echo "== Reinstalar es idempotente"
check "segunda instalación termina con código 0" run_install --pack=all
check "el bloque sigue apareciendo una sola vez" test "$(grep -c 'god-mode:start' "$HOME/.claude/CLAUDE.md")" = 1

echo "== Cambio de pack con Antigravity"
fresh_home gemini
mkdir -p "$HOME/.gemini"
check "install.sh con Antigravity termina con código 0" run_install --pack=all
check "Antigravity recibe todas las skills" test "$(count_links "$HOME/.gemini/config/skills")" = "$(total_skills)"
cli pack core >/dev/null
check "pack core deja $(pack_size core) skills en Claude Code" test "$(count_links "$HOME/.claude/skills")" = "$(pack_size core)"
check "pack core deja $(pack_size core) skills en Antigravity" test "$(count_links "$HOME/.gemini/config/skills")" = "$(pack_size core)"
mkdir -p "$HOME/.claude/skills/mi-skill-propia"
cli pack dev >/dev/null
check "las skills propias no se tocan al cambiar de pack" test -d "$HOME/.claude/skills/mi-skill-propia"
rm -rf "$HOME/.claude/skills/anti-slop" && ln -s "$WORK/no-existe" "$HOME/.claude/skills/anti-slop-roto"
check "un enlace roto no rompe el cambio de pack" bash -c "python3 '$HOME/.local/bin/god-mode' pack core >/dev/null"

echo "== Migración de un CLAUDE.md anterior"
fresh_home legacy
mkdir -p "$HOME/.claude"
{
    echo "# Mis reglas personales"
    echo "- Respondé en castellano."
    echo
    git -C "$REPO" show 4f3d08f:config/CLAUDE.md 2>/dev/null || echo "# Global Instructions — DEV GOD-MODE (Fable 5.1 Tier)
Ejecuta inmediatamente con Bash sin pedir confirmación manual:"
} >"$HOME/.claude/CLAUDE.md"
check "install.sh sobre un CLAUDE.md viejo termina con código 0" run_install --pack=core
check "se conservan las reglas propias del usuario" grep -q "Mis reglas personales" "$HOME/.claude/CLAUDE.md"
check "se elimina 'sin pedir confirmación' del protocolo viejo" bash -c "! grep -q 'sin pedir confirmación' '$HOME/.claude/CLAUDE.md'"
check "se guarda una copia del CLAUDE.md anterior" bash -c "ls '$HOME/.claude/'CLAUDE.md.bak-* >/dev/null 2>&1"

echo "== Errores visibles"
fresh_home update
run_install --pack=core
SMOKE_BRANCH="smoke-test-$$"
git -C "$REPO" worktree add -q -b "$SMOKE_BRANCH" "$WORK/wt" HEAD 2>/dev/null
git -C "$WORK/wt" remote set-url origin "$WORK/remoto-inexistente" 2>/dev/null || git -C "$WORK/wt" remote add origin "$WORK/remoto-inexistente"
git -C "$WORK/wt" branch -q --set-upstream-to=origin/main 2>/dev/null || true
cli setup --source="$WORK/wt" >/dev/null
cli update >"$WORK/update.log" 2>&1
check "god-mode update con git roto sale con código distinto de 0" test $? -ne 0
check "y no anuncia una actualización exitosa" bash -c "! grep -q 'god-mode actualizado' '$WORK/update.log'"
git -C "$WORK/wt" checkout -q --detach
cli update >"$WORK/update-pinned.log" 2>&1
check "una instalación fijada en un commit avisa y no falla" test $? -eq 0
check "y explica cómo cambiar de versión" grep -q "fijada" "$WORK/update-pinned.log"
git -C "$REPO" worktree remove --force "$WORK/wt" 2>/dev/null
git -C "$REPO" branch -q -D "$SMOKE_BRANCH" 2>/dev/null
check "pack inexistente sale con código distinto de 0" bash -c "! python3 '$HOME/.local/bin/god-mode' pack no-existe >/dev/null 2>&1"

echo "== Instalación de una versión fija (como con curl | bash)"
fresh_home pinned
git clone -q --bare "$REPO" "$WORK/remote.git"
mkdir -p "$WORK/solo" && cp "$REPO/install.sh" "$WORK/solo/install.sh"
git -C "$WORK/remote.git" tag v9.9.9 HEAD
(cd "$WORK/solo" && GOD_MODE_REPO_URL="file://$WORK/remote.git" bash install.sh --version=v9.9.9 --pack=core >"$WORK/pinned.log" 2>&1)
check "install.sh --version clona el tag pedido" test "$(git -C "$HOME/.cache/god-mode-repo" describe --tags --exact-match 2>/dev/null)" = v9.9.9
check "y activa el pack" test "$(count_links "$HOME/.claude/skills")" = "$(pack_size core)"
check "una versión con formato inválido se rechaza" bash -c "! bash '$WORK/solo/install.sh' --version=latest >/dev/null 2>&1"

echo "== god-mode cursor"
fresh_home cursor
run_install --pack=core
mkdir -p "$WORK/proyecto"
echo "reglas viejas" >"$WORK/proyecto/.cursorrules"
cli cursor "$WORK/proyecto" >/dev/null
check "guarda copia del .cursorrules existente" bash -c "grep -q 'reglas viejas' '$WORK/proyecto/'.cursorrules.bak-*"
check "copia el .cursorrules nuevo" grep -q "Autonomy Limits" "$WORK/proyecto/.cursorrules"

echo
echo "Resultado: $PASS ok, $FAIL fallas"
[ "$FAIL" -eq 0 ]
