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

SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9_.-]+$")
SAFE_SKILL_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
GITHUB_URL = re.compile(
    r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)"
    r"(?:/(?P<kind>tree|blob)/(?P<branch>[^/]+)(?:/(?P<subpath>.+?))?)?/?$"
)
CLONE_TIMEOUT_SECONDS = 300


class UnsafeInputError(ValueError):
    """Raised when a URL component could be used to escape the intended command or directory."""


def _check_segment(value, label):
    if (not value or not SAFE_SEGMENT.fullmatch(value) or value.startswith("-")
            or value in (".", "..") or ".." in value):
        raise UnsafeInputError(f"{label} con caracteres no permitidos: {value!r}")
    return value


def _check_subpath(subpath):
    parts = [part for part in subpath.strip("/").split("/") if part]
    for part in parts:
        _check_segment(part, "Segmento de ruta")
    return "/".join(parts) or None


def _is_within(path, root):
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False


def run_cmd(args, cwd=None):
    if not isinstance(args, (list, tuple)):
        raise TypeError("run_cmd requiere una lista de argumentos; nunca un string de shell")
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        res = subprocess.run(list(args), cwd=cwd, capture_output=True, text=True,
                             timeout=CLONE_TIMEOUT_SECONDS, env=env)
    except FileNotFoundError:
        return False, "", f"No se encontró el ejecutable '{args[0]}'"
    except subprocess.TimeoutExpired:
        return False, "", f"El comando superó el límite de {CLONE_TIMEOUT_SECONDS} segundos"
    return res.returncode == 0, res.stdout, res.stderr


def build_clone_cmd(info):
    cmd = ["git", "clone", "--depth", "1"]
    if info.get("branch"):
        cmd += ["--branch", info["branch"]]
    cmd += ["--", info["clone_url"], "repo"]
    return cmd

def parse_github_url(url):
    """
    Parses GitHub URLs into validated components:
    - https://github.com/owner/repo
    - https://github.com/owner/repo/tree/branch/sub/path
    - https://github.com/owner/repo/blob/branch/sub/path/SKILL.md
    - owner/repo

    Returns None for unrecognized formats and raises UnsafeInputError when a
    component contains characters that could reach a shell or escape the repo.
    """
    url = url.strip()
    if not url.startswith("http") and "/" in url and not url.startswith("git@"):
        url = f"https://github.com/{url}"

    m = GITHUB_URL.match(url)
    if not m:
        return None

    owner = _check_segment(m.group("owner"), "Owner")
    repo = m.group("repo")
    if repo.endswith(".git"):
        repo = repo[:-4]
    repo = _check_segment(repo, "Repositorio")

    branch = m.group("branch")
    if branch is not None:
        _check_segment(branch, "Rama")

    subpath = m.group("subpath")
    if subpath:
        if m.group("kind") == "blob" and subpath.endswith(".md"):
            parent = str(Path(subpath).parent)
            subpath = None if parent == "." else parent
        subpath = _check_subpath(subpath) if subpath else None

    return {
        "clone_url": f"https://github.com/{owner}/{repo}.git",
        "owner": owner,
        "repo": repo,
        "branch": branch,
        "subpath": subpath,
        "is_single_skill": m.group("kind") is not None,
    }

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

def _confirm_overwrite(skill_name, assume_yes):
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        log(f"'{skill_name}' ya existe. Para reemplazarla sin terminal interactiva, "
            "confirmá con el usuario y usá --force --yes.", "⛔")
        return False
    answer = input(f"¿Reemplazar la skill existente '{skill_name}'? [s/N] ").strip().lower()
    return answer in ("s", "si", "sí", "y", "yes")


def _escaping_symlinks(src):
    root = Path(src).resolve()
    return [p for p in Path(src).rglob("*") if p.is_symlink() and not _is_within(p, root)]


def install_skill_directory(src_skill_dir, skill_name=None, force=False, assume_yes=False):
    """Installs a skill directory into ~/.claude/skills and symlinks to ~/.gemini/config/skills."""
    src = Path(src_skill_dir)
    skill_file = src / "SKILL.md"
    if not skill_file.exists():
        log(f"No se encontró SKILL.md en {src}", "⚠️")
        return False

    if not skill_name:
        content = skill_file.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^name:\s*([a-zA-Z0-9_-]+)", content, re.MULTILINE)
        skill_name = m.group(1).strip() if m else src.name

    if not SAFE_SKILL_NAME.fullmatch(skill_name):
        log(f"Nombre de skill no permitido: {skill_name!r}", "⛔")
        return False

    escaping = _escaping_symlinks(src)
    if escaping:
        log(f"La skill '{skill_name}' contiene enlaces simbólicos que apuntan fuera de su carpeta "
            f"({', '.join(str(p.relative_to(src)) for p in escaping)}). Instalación cancelada.", "⛔")
        return False

    target_claude = CLAUDE_SKILLS / skill_name
    CLAUDE_SKILLS.mkdir(parents=True, exist_ok=True)
    GEMINI_SKILLS.mkdir(parents=True, exist_ok=True)

    if target_claude.exists() or target_claude.is_symlink():
        if not force:
            log(f"La skill '{skill_name}' ya existe en Claude Code. Usa --force para sobreescribir.", "ℹ️")
            return True
        if not _confirm_overwrite(skill_name, assume_yes):
            log(f"Se mantuvo la versión existente de '{skill_name}'.", "ℹ️")
            return False
        if target_claude.is_symlink() or target_claude.is_file():
            target_claude.unlink()
        else:
            shutil.rmtree(target_claude)
        log(f"Reemplazando versión existente de {skill_name} (--force confirmado)", "🔄")

    shutil.copytree(src, target_claude, symlinks=True)
    log(f"Skill instalada en Claude Code: {target_claude}", "✅")

    target_gemini = GEMINI_SKILLS / skill_name
    if not target_gemini.exists():
        try:
            target_gemini.symlink_to(target_claude, target_is_directory=True)
            log(f"Skill sincronizada con Antigravity: {target_gemini}", "🔗")
        except Exception as e:
            log(f"Aviso al vincular con Antigravity: {e}", "⚠️")

    return True

def install_from_github(url, force=False, assume_yes=False):
    try:
        info = parse_github_url(url)
    except UnsafeInputError as e:
        log(f"URL rechazada por seguridad: {e}", "⛔")
        return False
    if not info:
        log(f"Formato de URL no reconocido: {url}", "❌")
        return False

    with tempfile.TemporaryDirectory(prefix="skill_install_") as tmpdir:
        tmp_path = Path(tmpdir)
        log(f"Clonando repositorio {info['clone_url']}...", "📥")

        ok, out, err = run_cmd(build_clone_cmd(info), cwd=tmpdir)
        if not ok:
            log(f"Error al clonar repositorio: {err.strip()}", "❌")
            return False

        repo_dir = tmp_path / "repo"
        search_root = repo_dir
        if info.get("subpath"):
            candidate = repo_dir / info["subpath"]
            if not _is_within(candidate, repo_dir):
                log(f"La ruta {info['subpath']!r} sale del repositorio. Instalación cancelada.", "⛔")
                return False
            if not candidate.is_dir():
                log(f"La ruta {info['subpath']!r} no existe en el repositorio.", "❌")
                return False
            search_root = candidate

        if (search_root / "SKILL.md").exists():
            return install_skill_directory(search_root, skill_name=search_root.name,
                                           force=force, assume_yes=assume_yes)

        found_skills = list(search_root.glob("**/SKILL.md"))
        if not found_skills:
            log(f"No se encontraron archivos SKILL.md en {url}", "❌")
            return False

        log(f"Se encontraron {len(found_skills)} skill(s) en el repositorio:", "📦")
        installed_count = 0
        for sk in found_skills:
            if install_skill_directory(sk.parent, force=force, assume_yes=assume_yes):
                installed_count += 1

        failed = len(found_skills) - installed_count
        log(f"Instalación finalizada: {installed_count} skill(s) operativas, {failed} con errores.",
            "🎉" if failed == 0 else "⚠️")
        return installed_count > 0

def main():
    if len(sys.argv) < 2:
        print("""
Uso:
  python3 install-skill.py <github-url-o-repo> [--force [--yes]]
  python3 install-skill.py --search <termino>

Ejemplos:
  python3 install-skill.py https://github.com/VoltAgent/awesome-agent-skills
  python3 install-skill.py https://github.com/officialzeroxyz/zero-plugins/tree/main/plugins/zero/skills/zero
  python3 install-skill.py --search duckdb
  python3 install-skill.py --search linkedin
        """)
        sys.exit(1)

    force = "--force" in sys.argv
    assume_yes = "--yes" in sys.argv
    args = [a for a in sys.argv[1:] if a not in ("--force", "--yes")]
    if not args:
        log("Falta la URL o el término de búsqueda.", "❌")
        sys.exit(1)

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
    success = install_from_github(url_or_repo, force=force, assume_yes=assume_yes)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
