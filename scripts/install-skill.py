#!/usr/bin/env python3
"""
DEV GOD-MODE Skill Installer for Claude Code & Antigravity
Installs Agent Skills from GitHub repos, subfolders, raw URLs, or VoltAgent/awesome-agent-skills.
Syncs automatically to both ~/.claude/skills/ and ~/.gemini/config/skills/.
"""

import sys
import os
import re
import shutil
import tempfile
import subprocess
import urllib.request
from pathlib import Path

CLAUDE_SKILLS = Path.home() / ".claude" / "skills"
GEMINI_SKILLS = Path.home() / ".gemini" / "config" / "skills"
AWESOME_REPO_README = "https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main/README.md"

def log(msg, emoji="⚡"):
    print(f"{emoji} {msg}")

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode == 0, res.stdout, res.stderr

def parse_github_url(url):
    """
    Parses various GitHub URL formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo/tree/branch/sub/path
    - https://github.com/owner/repo/blob/branch/sub/path/SKILL.md
    - owner/repo
    """
    url = url.strip()
    if not url.startswith("http") and "/" in url and not url.startswith("git@"):
        url = f"https://github.com/{url}"

    # Pattern for tree / subpath
    m_tree = re.match(r"https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)", url)
    if m_tree:
        owner, repo, branch, subpath = m_tree.groups()
        return {
            "clone_url": f"https://github.com/{owner}/{repo}.git",
            "owner": owner,
            "repo": repo.replace(".git", ""),
            "branch": branch,
            "subpath": subpath,
            "is_single_skill": True
        }

    # Pattern for blob
    m_blob = re.match(r"https?://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)", url)
    if m_blob:
        owner, repo, branch, subpath = m_blob.groups()
        subpath_dir = str(Path(subpath).parent) if subpath.endswith(".md") else subpath
        return {
            "clone_url": f"https://github.com/{owner}/{repo}.git",
            "owner": owner,
            "repo": repo.replace(".git", ""),
            "branch": branch,
            "subpath": subpath_dir,
            "is_single_skill": True
        }

    # Pattern for base repo
    m_repo = re.match(r"https?://github\.com/([^/]+)/([^/]+)", url)
    if m_repo:
        owner, repo = m_repo.groups()
        return {
            "clone_url": f"https://github.com/{owner}/{repo}.git" if not repo.endswith(".git") else f"https://github.com/{owner}/{repo}",
            "owner": owner,
            "repo": repo.replace(".git", ""),
            "branch": None,
            "subpath": None,
            "is_single_skill": False
        }

    return None

def search_awesome_skills(query):
    log(f"Buscando '{query}' en VoltAgent/awesome-agent-skills...", "🔍")
    try:
        req = urllib.request.Request(AWESOME_REPO_README, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8')
    except Exception as e:
        log(f"Error accediendo a awesome-agent-skills: {e}", "❌")
        return []

    # Find matches in markdown links: - **[name](url)** - description
    matches = []
    lines = content.splitlines()
    q = query.lower()
    for line in lines:
        if q in line.lower() and "[" in line and "](" in line:
            m = re.search(r"-\s+\*\*\[(.*?)\]\((.*?)\)\*\*\s*-\s*(.*)", line)
            if m:
                name, url, desc = m.groups()
                matches.append({"name": name, "url": url, "description": desc})
            else:
                m2 = re.search(r"\[(.*?)\]\((.*?)\)", line)
                if m2:
                    name, url = m2.groups()
                    matches.append({"name": name, "url": url, "description": line})
    return matches

def install_skill_directory(src_skill_dir, skill_name=None, force=False):
    """Installs a skill directory into ~/.claude/skills and symlinks to ~/.gemini/config/skills."""
    src = Path(src_skill_dir)
    skill_file = src / "SKILL.md"
    if not skill_file.exists():
        log(f"No se encontró SKILL.md en {src}", "⚠️")
        return False

    # Extract name from YAML frontmatter if not specified
    if not skill_name:
        content = skill_file.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^name:\s*([a-zA-Z0-9_-]+)", content, re.MULTILINE)
        if m:
            skill_name = m.group(1).strip()
        else:
            skill_name = src.name

    target_claude = CLAUDE_SKILLS / skill_name
    CLAUDE_SKILLS.mkdir(parents=True, exist_ok=True)
    GEMINI_SKILLS.mkdir(parents=True, exist_ok=True)

    if target_claude.exists():
        if force:
            if target_claude.is_symlink() or target_claude.is_file():
                target_claude.unlink()
            else:
                shutil.rmtree(target_claude)
            log(f"Reemplazando versión existente de {skill_name} (--force activo)", "🔄")
        else:
            log(f"La skill '{skill_name}' ya existe en Claude Code. Usa --force para sobreescribir.", "ℹ️")
            return True

    # Copy to Claude Skills directory
    shutil.copytree(src, target_claude)
    log(f"Skill instalada en Claude Code: {target_claude}", "✅")

    # Symlink to Antigravity (~/.gemini/config/skills/)
    target_gemini = GEMINI_SKILLS / skill_name
    if not target_gemini.exists():
        try:
            target_gemini.symlink_to(target_claude, target_is_directory=True)
            log(f"Skill sincronizada con Antigravity: {target_gemini}", "🔗")
        except Exception as e:
            log(f"Aviso al vincular con Antigravity: {e}", "⚠️")

    return True

def install_from_github(url, force=False):
    info = parse_github_url(url)
    if not info:
        log(f"Formato de URL no reconocido: {url}", "❌")
        return False

    with tempfile.TemporaryDirectory(prefix="skill_install_") as tmpdir:
        tmp_path = Path(tmpdir)
        log(f"Clonando repositorio {info['clone_url']}...", "📥")
        
        branch_flag = f"-b {info['branch']}" if info.get('branch') else ""
        ok, out, err = run_cmd(f"git clone --depth 1 {branch_flag} {info['clone_url']} repo", cwd=tmpdir)
        if not ok:
            log(f"Error al clonar repositorio: {err.strip()}", "❌")
            return False

        repo_dir = tmp_path / "repo"
        search_root = repo_dir
        if info.get('subpath'):
            candidate = repo_dir / info['subpath']
            if candidate.exists():
                search_root = candidate

        # Check if search_root itself is a skill
        if (search_root / "SKILL.md").exists():
            return install_skill_directory(search_root, skill_name=search_root.name, force=force)

        # Scan for all SKILL.md files inside
        found_skills = list(search_root.glob("**/SKILL.md"))
        if not found_skills:
            log(f"No se encontraron archivos SKILL.md en {url}", "❌")
            return False

        log(f"Se encontraron {len(found_skills)} skill(s) en el repositorio:", "📦")
        installed_count = 0
        for sk in found_skills:
            sk_dir = sk.parent
            if install_skill_directory(sk_dir, force=force):
                installed_count += 1

        log(f"Instalación finalizada: {installed_count} skill(s) operativas.", "🎉")
        return True

def main():
    if len(sys.argv) < 2:
        print("""
Uso:
  python3 install-skill.py <github-url-o-repo> [--force]
  python3 install-skill.py --search <termino>

Ejemplos:
  python3 install-skill.py https://github.com/VoltAgent/awesome-agent-skills
  python3 install-skill.py https://github.com/officialzeroxyz/zero-plugins/tree/main/plugins/zero/skills/zero
  python3 install-skill.py --search duckdb
  python3 install-skill.py --search linkedin
        """)
        sys.exit(1)

    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]

    if args[0] == "--search":
        if len(args) < 2:
            log("Especifica un término de búsqueda. Ej: --search stripe", "❌")
            sys.exit(1)
        query = args[1]
        matches = search_awesome_skills(query)
        if not matches:
            log(f"No se encontraron skills para '{query}' en VoltAgent/awesome-agent-skills.", "ℹ️")
        else:
            log(f"Coincidencias encontradas ({len(matches)}):", "🎯")
            for idx, m in enumerate(matches, 1):
                print(f"  {idx}. {m['name']}")
                print(f"     URL: {m['url']}")
                print(f"     Desc: {m['description']}")
            print("\nPara instalar una de ellas ejecuta:")
            print(f"  python3 ~/.claude/scripts/install-skill.py <URL>")
        sys.exit(0)

    url_or_repo = args[0]
    success = install_from_github(url_or_repo, force=force)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
