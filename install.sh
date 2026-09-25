#!/usr/bin/env bash
# ==============================================================================
# Arcadia GOD-Tier 1-Click Installer for Claude Code & Google Antigravity
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

echo -e "${PURPLE}${BOLD}"
cat << 'EOF'
     ___    ____   ____    _    ____ ___    _        ____  ___  ____
    /   \  |  _ \ / ___|  / \  |  _ \_ _|  / \      / ___|/ _ \|  _ \
   / /_\ \ | |_) | |     / _ \ | | | | |  / _ \    | |  _| | | | | | |
  / _____ \|  _ <| |___ / ___ \| |_| | | / ___ \   | |_| | |_| | |_| |
 /_/     \_\_| \_\\____/_/   \_\____/___/_/   \_\   \____|\___/|____/
                   T I E R   —   F A B L E   5 . 1
EOF
echo -e "${NC}"
echo -e "${CYAN}⚡ The Autonomous GOD-Tier Suite for Antigravity & Claude Code${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Determine directory of this script or clone repo if running from curl
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TMP_CLONE_DIR=""

if [ ! -d "$SCRIPT_DIR/skills" ]; then
    echo -e "${YELLOW}📥 Fetching latest release from GitHub...${NC}"
    TMP_CLONE_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/Gastonchevarria/god-mode.git "$TMP_CLONE_DIR" >/dev/null 2>&1 || {
        echo -e "${RED}❌ Error cloning repository. Ensure git and internet connection are available.${NC}"
        exit 1
    }
    SCRIPT_DIR="$TMP_CLONE_DIR"
fi

CLAUDE_DIR="$HOME/.claude"
GEMINI_DIR="$HOME/.gemini/config"

echo -e "\n${BOLD}🔍 Detecting installed AI coding environments...${NC}"

HAS_CLAUDE=false
HAS_GEMINI=false

if [ -d "$CLAUDE_DIR" ] || command -v claude >/dev/null 2>&1; then
    HAS_CLAUDE=true
    echo -e "  ${GREEN}✓ Claude Code detected${NC} ($CLAUDE_DIR)"
else
    echo -e "  ${YELLOW}○ Claude Code not found (creating target directory)${NC}"
    mkdir -p "$CLAUDE_DIR"
    HAS_CLAUDE=true
fi

if [ -d "$GEMINI_DIR" ] || [ -d "$HOME/.gemini" ]; then
    HAS_GEMINI=true
    echo -e "  ${GREEN}✓ Google Antigravity detected${NC} ($GEMINI_DIR)"
else
    echo -e "  ${YELLOW}○ Google Antigravity directory prepared${NC} ($GEMINI_DIR)"
    mkdir -p "$GEMINI_DIR"
    HAS_GEMINI=true
fi

# 1. Install to Claude Code
echo -e "\n${BOLD}🚀 [1/3] Installing 130+ Skills & Subagents into Claude Code...${NC}"
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/scripts"

cp -R "$SCRIPT_DIR"/skills/* "$CLAUDE_DIR/skills/"
cp -R "$SCRIPT_DIR"/agents/* "$CLAUDE_DIR/agents/"
if [ -d "$SCRIPT_DIR/scripts" ]; then
    cp -R "$SCRIPT_DIR"/scripts/* "$CLAUDE_DIR/scripts/"
fi
chmod +x "$CLAUDE_DIR"/scripts/*.py 2>/dev/null || true

# Update or install ~/.claude/CLAUDE.md
if [ -f "$SCRIPT_DIR/config/CLAUDE.md" ]; then
    if [ ! -f "$CLAUDE_DIR/CLAUDE.md" ]; then
        cp "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
        echo -e "  ${GREEN}✓ Created global ~/.claude/CLAUDE.md${NC}"
    else
        # Append router if not present
        if ! grep -q "Startup GOD Router" "$CLAUDE_DIR/CLAUDE.md"; then
            echo "" >> "$CLAUDE_DIR/CLAUDE.md"
            cat "$SCRIPT_DIR/config/CLAUDE.md" >> "$CLAUDE_DIR/CLAUDE.md"
            echo -e "  ${GREEN}✓ Integrated GOD Router into existing ~/.claude/CLAUDE.md${NC}"
        else
            echo -e "  ${BLUE}ℹ Existing GOD Router found in ~/.claude/CLAUDE.md${NC}"
        fi
    fi
fi

# 2. Sync to Google Antigravity
echo -e "\n${BOLD}🔗 [2/3] Establishing Zero-Drift Sync with Antigravity...${NC}"
mkdir -p "$GEMINI_DIR/skills"
mkdir -p "$GEMINI_DIR/scripts"

# Create symlinks from Claude skills to Antigravity so they share single source of truth
for skill in "$CLAUDE_DIR"/skills/*; do
    skill_name=$(basename "$skill")
    if [ ! -e "$GEMINI_DIR/skills/$skill_name" ]; then
        ln -s "$skill" "$GEMINI_DIR/skills/$skill_name" 2>/dev/null || cp -R "$skill" "$GEMINI_DIR/skills/"
    fi
done

if [ -f "$SCRIPT_DIR/config/GEMINI_RULES.md" ]; then
    mkdir -p "$GEMINI_DIR/rules"
    cp "$SCRIPT_DIR/config/GEMINI_RULES.md" "$GEMINI_DIR/rules/arcadia_god.md"
    echo -e "  ${GREEN}✓ Created Antigravity Global Rules in ~/.gemini/config/rules/arcadia_god.md${NC}"
fi

# Clean up temp clone if used
if [ -n "$TMP_CLONE_DIR" ] && [ -d "$TMP_CLONE_DIR" ]; then
    rm -rf "$TMP_CLONE_DIR"
fi

echo -e "\n${BOLD}✨ [3/3] Verifying Installation...${NC}"
SKILL_COUNT=$(ls -1 "$CLAUDE_DIR/skills" | wc -l | tr -d ' ')
AGENT_COUNT=$(ls -1 "$CLAUDE_DIR/agents" | wc -l | tr -d ' ')

echo -e "  ${GREEN}✓ ${SKILL_COUNT} Production Skills Active${NC}"
echo -e "  ${GREEN}✓ ${AGENT_COUNT} Autonomous Subagents Deployed${NC}"
echo -e "  ${GREEN}✓ Fable 5.1 Protocol Injected${NC}"
echo -e "  ${GREEN}✓ Autonomous GitHub Skill Downloader Ready${NC}"

echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}${BOLD}🎉 SUCCESS! Arcadia GOD-Tier is fully operational.${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "To activate in Claude Code, open your project terminal and run:"
echo -e "  ${BOLD}claude${NC}"
echo -e "  Type: ${CYAN}/god${NC} or ${CYAN}/startup-god-router${NC}"
echo -e ""
echo -e "Available Quick Commands:"
echo -e "  ${CYAN}/thermos${NC}        ➔ Pre-merge double thermo-nuclear code review"
echo -e "  ${CYAN}/anti-slop${NC}      ➔ Remove lazy AI patterns and sanitize code"
echo -e "  ${CYAN}/security${NC}       ➔ DevSecOps pre-launch security audit"
echo -e "  ${CYAN}/archify${NC}        ➔ Interactive HTML/SVG system architecture"
echo -e "  ${CYAN}/validate${NC}       ➔ Validate startup ideas, ICP & JTBD"
echo -e "  ${CYAN}/monetize${NC}       ➔ SaaS business models, pricing & Stripe"
echo -e "  ${CYAN}/scope-kill${NC}     ➔ Ruthless MVP scope cutter"
echo -e "  ${CYAN}/install-skill${NC}  ➔ Install any skill from GitHub automatically"
echo -e ""
echo -e "${YELLOW}⭐ If you love this suite, give it a star on GitHub:${NC}"
echo -e "${BOLD}https://github.com/Gastonchevarria/god-mode${NC}\n"
