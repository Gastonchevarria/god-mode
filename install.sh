#!/usr/bin/env bash
# ==============================================================================
# DEV GOD-MODE Installer for Claude Code, Antigravity, Cursor & Windsurf
# ==============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

CURRENT_STEP="inicio"
trap 'echo -e "\n${RED}❌ La instalación falló durante: ${CURRENT_STEP}. No se completaron los pasos siguientes.${NC}" >&2' ERR

PACK="core"
WITH_CURSOR=false
VERSION=""
REPO_URL="${GOD_MODE_REPO_URL:-https://github.com/Gastonchevarria/god-mode.git}"

for arg in "$@"; do
    case $arg in
        --pack=*) PACK="${arg#*=}" ;;
        --cursor) WITH_CURSOR=true ;;
        --version=*) VERSION="${arg#*=}" ;;
        --help|-h)
            echo "Uso: ./install.sh [--pack=core|dev|growth|all] [--cursor] [--version=vX.Y.Z]"
            echo "  --pack=<nombre>  Pack de skills a activar (por defecto: core). 'god-mode status' muestra cuántas trae cada uno."
            echo "  --cursor         Además copia .cursorrules y AGENTS.md a la carpeta actual (guarda copia de los existentes)."
            echo "  --version=vX.Y.Z Instala una versión publicada en lugar de la rama main."
            exit 0
            ;;
        *) echo -e "${RED}Opción desconocida: $arg (usá --help)${NC}" >&2; exit 1 ;;
    esac
done

if [ -n "$VERSION" ] && ! [[ "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ Versión inválida: $VERSION (formato esperado: v1.2.3)${NC}" >&2
    exit 1
fi

command -v git >/dev/null 2>&1 || { echo -e "${RED}❌ Se necesita git instalado.${NC}" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}❌ Se necesita python3 instalado.${NC}" >&2; exit 1; }

echo -e "${PURPLE}${BOLD}"
cat << 'EOF'
  ____  _______     __   ____  ___  ____        __  __  ___  ____  _____ 
 |  _ \| ____\ \   / /  / ___|/ _ \|  _ \      |  \/  |/ _ \|  _ \| ____|
 | | | |  _|  \ \ / /  | |  _| | | | | | |_____| |\/| | | | | | | |  _|  
 | |_| | |___  \ V /   | |_| | |_| | |_| |_____| |  | | |_| | |_| | |___ 
 |____/|_____|  \_/     \____|\___/|____/      |_|  |_|\___/|____/|_____|
                        F A B L E   5 . 1   T I E R
EOF
echo -e "${NC}"
echo -e "${CYAN}⚡ The Autonomous DEV GOD-MODE Suite for Claude Code, Cursor, Antigravity & Windsurf${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"


# Replace the cache only after the new clone succeeded, and never leave it half-deleted.
swap_cache() {
    rm -rf "$CACHE_REPO.old"
    if [ -e "$CACHE_REPO" ]; then mv "$CACHE_REPO" "$CACHE_REPO.old"; fi
    mv "$CACHE_REPO.tmp" "$CACHE_REPO"
    rm -rf "$CACHE_REPO.old"
}

CURRENT_STEP="descarga del repositorio"
# With `curl ... | bash` there is no script file: BASH_SOURCE is empty and $0 is "bash", so never
# fall back to the current directory, which may be an unrelated or outdated checkout.
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi
CACHE_REPO="$HOME/.cache/god-mode-repo"

if [ -z "$SCRIPT_DIR" ] || [ ! -f "$SCRIPT_DIR/config/packs.json" ]; then
    if [ -n "$VERSION" ]; then
        echo -e "${YELLOW}📥 Descargando god-mode $VERSION desde GitHub...${NC}"
        rm -rf "$CACHE_REPO.tmp"
        mkdir -p "$(dirname "$CACHE_REPO")"
        git clone --depth 1 --branch "$VERSION" -- "$REPO_URL" "$CACHE_REPO.tmp"
        swap_cache
    elif [ -d "$CACHE_REPO/.git" ] && git -C "$CACHE_REPO" symbolic-ref -q HEAD >/dev/null; then
        echo -e "${YELLOW}📥 Actualizando la copia local de god-mode...${NC}"
        git -C "$CACHE_REPO" pull --ff-only
    else
        echo -e "${YELLOW}📥 Descargando god-mode desde GitHub...${NC}"
        rm -rf "$CACHE_REPO.tmp"
        mkdir -p "$(dirname "$CACHE_REPO")"
        git clone --depth 1 -- "$REPO_URL" "$CACHE_REPO.tmp"
        swap_cache
    fi
    SCRIPT_DIR="$CACHE_REPO"
elif [ -n "$VERSION" ]; then
    echo -e "${YELLOW}⚠️  --version se ignora al instalar desde una copia local ($SCRIPT_DIR).${NC}"
fi

if ! python3 -c 'import json,sys; sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1]))["packs"] else 1)' \
        "$SCRIPT_DIR/config/packs.json" "$PACK"; then
    echo -e "${RED}❌ Pack desconocido: $PACK. Opciones: $(python3 -c 'import json,sys; print(", ".join(json.load(open(sys.argv[1]))["packs"]))' "$SCRIPT_DIR/config/packs.json")${NC}" >&2
    exit 1
fi

CURRENT_STEP="detección de entornos"
echo -e "\n${BOLD}🔍 Detectando entornos de IA...${NC}"
TARGETS="claude"
if [ -d "$HOME/.claude" ] || command -v claude >/dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Claude Code detectado${NC}"
else
    echo -e "  ${BLUE}ℹ Claude Code no detectado: se instala igual en ~/.claude${NC}"
fi
if [ -d "$HOME/.gemini" ]; then
    TARGETS="claude,gemini"
    echo -e "  ${GREEN}✓ Google Antigravity detectado${NC}"
fi
if [ -d "$HOME/.cursor" ] || command -v cursor >/dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Cursor detectado${NC} (usá --cursor o 'god-mode cursor <proyecto>' para copiar las reglas)"
fi

CURRENT_STEP="instalación del CLI"
echo -e "\n${BOLD}⚙️  [1/3] Instalando el CLI 'god-mode'...${NC}"
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
cp "$SCRIPT_DIR/bin/god-mode" "$LOCAL_BIN/god-mode"
chmod +x "$LOCAL_BIN/god-mode"
echo -e "  ${GREEN}✓ $LOCAL_BIN/god-mode${NC}"

CURRENT_STEP="protocolo y subagentes"
echo -e "\n${BOLD}🧠 [2/3] Protocolo Fable 5.1, subagentes e instalador de skills...${NC}"
python3 "$LOCAL_BIN/god-mode" setup --targets="$TARGETS" --source="$SCRIPT_DIR"

if [ "$WITH_CURSOR" = true ]; then
    CURRENT_STEP="reglas de Cursor"
    python3 "$LOCAL_BIN/god-mode" cursor "."
fi

CURRENT_STEP="activación del pack $PACK"
echo -e "\n${BOLD}📦 [3/3] Activando el pack ${CYAN}${PACK}${NC}..."
python3 "$LOCAL_BIN/god-mode" pack "$PACK"

trap - ERR

if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}💡 Agregá ~/.local/bin a tu PATH para usar 'god-mode' desde cualquier lugar:${NC}"
    echo -e "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
fi

echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${BOLD}🎉 DEV GOD-MODE instalado.${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Comandos principales:"
echo -e "  ${CYAN}/god${NC}                      ➔ Orquestador: elige las skills según tu pedido"
echo -e "  ${CYAN}/thermos${NC}                  ➔ Doble revisión pre-merge (bugs + calidad)"
echo -e "  ${CYAN}/anti-slop${NC}                ➔ Limpia código vago y tipos flojos"
echo -e "  ${CYAN}/security${NC}                 ➔ Auditoría de seguridad pre-launch"
echo -e "  ${CYAN}/archify${NC}                  ➔ Diagrama interactivo de arquitectura"
echo -e ""
echo -e "CLI:"
echo -e "  ${BOLD}god-mode status${NC}           ➔ Pack activo y cantidades"
echo -e "  ${BOLD}god-mode pack <nombre>${NC}    ➔ Cambiar de pack"
echo -e "  ${BOLD}god-mode update${NC}           ➔ Actualizar desde GitHub"
echo -e "  ${BOLD}god-mode cursor <ruta>${NC}    ➔ Copiar reglas a un proyecto de Cursor"
echo -e ""
echo -e "${BOLD}https://github.com/Gastonchevarria/god-mode${NC}\n"
