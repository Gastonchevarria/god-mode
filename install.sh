#!/usr/bin/env bash
# ==============================================================================
# DEV GOD-MODE 1-Click Installer for Claude Code, Antigravity, Cursor & Windsurf
# ==============================================================================

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Default pack to prevent Context Bloat
PACK="core"

# Parse CLI arguments
for arg in "$@"; do
    case $arg in
        --pack=*)
            PACK="${arg#*=}"
            shift
            ;;
        --help|-h)
            echo "Uso: ./install.sh [--pack=core|dev|growth|all]"
            echo "  --pack=core     (Default) 20 skills indispensables (Cero ruido de contexto)"
            echo "  --pack=dev      57 skills Fullstack, Backend, AI Pipelines, Testing"
            echo "  --pack=growth   72 skills SaaS Growth, Monetización, SEO, CRO, Ads"
            echo "  --pack=all      135 skills completas"
            exit 0
            ;;
    esac
done

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

# Determine directory of this script or clone repo if running from curl
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CACHE_REPO="$HOME/.cache/god-mode-repo"

if [ ! -d "$SCRIPT_DIR/skills" ]; then
    echo -e "${YELLOW}📥 Descargando última versión de god-mode desde GitHub...${NC}"
    mkdir -p "$CACHE_REPO"
    if [ -d "$CACHE_REPO/.git" ]; then
        cd "$CACHE_REPO" && git pull --rebase >/dev/null 2>&1 || true
    else
        git clone --depth 1 https://github.com/Gastonchevarria/god-mode.git "$CACHE_REPO" >/dev/null 2>&1
    fi
    SCRIPT_DIR="$CACHE_REPO"
fi

CLAUDE_DIR="$HOME/.claude"
GEMINI_DIR="$HOME/.gemini/config"
LOCAL_BIN="$HOME/.local/bin"

echo -e "\n${BOLD}🔍 Detectando entornos de IA compatibles...${NC}"

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents" "$CLAUDE_DIR/scripts"
mkdir -p "$GEMINI_DIR/skills" "$GEMINI_DIR/rules" "$GEMINI_DIR/scripts"
mkdir -p "$LOCAL_BIN"

if [ -d "$CLAUDE_DIR" ] || command -v claude >/dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Claude Code detectado${NC}"
fi

if [ -d "$GEMINI_DIR" ] || [ -d "$HOME/.gemini" ]; then
    echo -e "  ${GREEN}✓ Google Antigravity detectado${NC}"
fi

# Cursor detection
HAS_CURSOR=false
if [ -d "$HOME/.cursor" ] || [ -f ".cursorrules" ] || command -v cursor >/dev/null 2>&1; then
    HAS_CURSOR=true
    echo -e "  ${GREEN}✓ Cursor IDE detectado${NC}"
fi

# 1. Instalar CLI global 'god-mode'
echo -e "\n${BOLD}⚙️  [1/4] Instalando CLI global 'god-mode'...${NC}"
if [ -f "$SCRIPT_DIR/bin/god-mode" ]; then
    cp "$SCRIPT_DIR/bin/god-mode" "$LOCAL_BIN/god-mode"
    chmod +x "$LOCAL_BIN/god-mode"
    
    # Intentar instalar en /usr/local/bin si tiene permisos
    if [ -w "/usr/local/bin" ]; then
        cp "$SCRIPT_DIR/bin/god-mode" "/usr/local/bin/god-mode" 2>/dev/null || true
    fi
    echo -e "  ${GREEN}✓ Comando global 'god-mode' instalado en $LOCAL_BIN/god-mode${NC}"
fi

# Instalar script de descarga de skills
if [ -f "$SCRIPT_DIR/scripts/install-skill.py" ]; then
    cp "$SCRIPT_DIR/scripts/install-skill.py" "$CLAUDE_DIR/scripts/"
    chmod +x "$CLAUDE_DIR/scripts/install-skill.py"
fi

# 2. Configuración Fable 5.1 & Reglas
echo -e "\n${BOLD}🧠 [2/4] Configurando protocolo Fable 5.1 & GOD Router...${NC}"

# Claude Code
if [ -f "$SCRIPT_DIR/config/CLAUDE.md" ]; then
    if [ ! -f "$CLAUDE_DIR/CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
        echo -e "  ${GREEN}✓ Creado ~/.claude/CLAUDE.md${NC}"
    elif ! grep -q "Startup GOD Router" "$CLAUDE_DIR/CLAUDE.md"; then
        echo "" >> "$CLAUDE_DIR/CLAUDE.md"
        cat "$SCRIPT_DIR/config/CLAUDE.md" >> "$CLAUDE_DIR/CLAUDE.md"
        echo -e "  ${GREEN}✓ Integrado GOD Router en ~/.claude/CLAUDE.md${NC}"
    else
        echo -e "  ${BLUE}ℹ Router ya presente en ~/.claude/CLAUDE.md${NC}"
    fi
fi

# Antigravity Rules
if [ -f "$SCRIPT_DIR/config/GEMINI_RULES.md" ]; then
    cp "$SCRIPT_DIR/config/GEMINI_RULES.md" "$GEMINI_DIR/rules/dev_god_mode.md"
    echo -e "  ${GREEN}✓ Creado ~/.gemini/config/rules/dev_god_mode.md${NC}"
fi

# Cursor & Windsurf rules en proyecto actual
if [ -f "$SCRIPT_DIR/config/.cursorrules" ]; then
    cp "$SCRIPT_DIR/config/.cursorrules" "./.cursorrules"
    cp "$SCRIPT_DIR/config/AGENTS.md" "./AGENTS.md"
    echo -e "  ${GREEN}✓ Generados .cursorrules y AGENTS.md en el proyecto actual${NC}"
fi

# 3. Copiar subagentes
echo -e "\n${BOLD}🤖 [3/4] Desplegando 6 Subagentes Especializados...${NC}"
if [ -d "$SCRIPT_DIR/agents" ]; then
    for ag in "$SCRIPT_DIR"/agents/*; do
        ag_name=$(basename "$ag")
        rm -f "$CLAUDE_DIR/agents/$ag_name" 2>/dev/null || true
        cp "$ag" "$CLAUDE_DIR/agents/$ag_name"
    done
    echo -e "  ${GREEN}✓ Subagentes instalados en ~/.claude/agents/${NC}"
fi

# 4. Aplicar Pack Seleccionado (Anti Context Bloat)
PACK_UPPER=$(echo "$PACK" | tr '[:lower:]' '[:upper:]')
echo -e "\n${BOLD}📦 [4/4] Aplicando Pack Modular: ${CYAN}${PACK_UPPER}${NC}..."
if [ -x "$LOCAL_BIN/god-mode" ]; then
    "$LOCAL_BIN/god-mode" pack "$PACK"
else
    python3 "$SCRIPT_DIR/bin/god-mode" pack "$PACK"
fi

# PATH check reminder
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}💡 Tip: Agrega ~/.local/bin a tu PATH para usar 'god-mode' desde cualquier lugar:${NC}"
    echo -e "   export PATH=\"\$HOME/.local/bin:\$PATH\" >> ~/.zshrc (o ~/.bashrc)"
fi

echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${BOLD}🎉 SUCCESS! DEV GOD-MODE está 100% operativo en tu sistema.${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Comandos Disponibles de la Suite:"
echo -e "  ${CYAN}/god${NC} o ${CYAN}/startup-god-router${NC}  ➔ Meta-Orquestador Inteligente"
echo -e "  ${CYAN}/thermos${NC}                  ➔ Pre-merge double thermo-nuclear code review"
echo -e "  ${CYAN}/anti-slop${NC}                ➔ Purga vicios, lazy types y código vago de IA"
echo -e "  ${CYAN}/security${NC}                 ➔ DevSecOps pre-launch defensive audit"
echo -e "  ${CYAN}/archify${NC}                  ➔ Diagrama interactivo HTML/SVG de arquitectura"
echo -e "  ${CYAN}/validate${NC}                 ➔ Validación de hipótesis e ICP"
echo -e "  ${CYAN}/monetize${NC}                 ➔ Modelos de cobro, pricing y Stripe"
echo -e "  ${CYAN}/scope-kill${NC}               ➔ Poda radical de MVP"
echo -e ""
echo -e "Gestión con el nuevo CLI 'god-mode':"
echo -e "  ${BOLD}god-mode status${NC}           ➔ Ver pack activo y estadísticas"
echo -e "  ${BOLD}god-mode pack dev${NC}         ➔ Cambiar a pack Fullstack & AI"
echo -e "  ${BOLD}god-mode pack growth${NC}      ➔ Cambiar a pack Growth & Marketing"
echo -e "  ${BOLD}god-mode update${NC}           ➔ Actualizar suite desde GitHub"
echo -e "  ${BOLD}god-mode cursor${NC}           ➔ Inyectar reglas en cualquier proyecto Cursor"
echo -e ""
echo -e "${YELLOW}⭐ Apoya el proyecto con una Estrella en GitHub:${NC}"
echo -e "${BOLD}https://github.com/Gastonchevarria/god-mode${NC}\n"
