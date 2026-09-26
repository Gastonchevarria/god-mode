#!/usr/bin/env python3
"""
Repository validator for god-mode. Run from the repo root:

    python3 scripts/validate.py [--max-description N]

Exits 1 and lists every problem found. Used by CI on every pull request.
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
DEFAULT_MAX_DESCRIPTION = 300
# Skills allowed to set disable-model-invocation (manual-only). Keep empty unless a skill must never auto-run.
MANUAL_ONLY_ALLOWLIST = set()


def read_frontmatter(path, errors):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER.match(text)
    if not m:
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML frontmatter ({e})")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)}: frontmatter is not a mapping")
        return None
    return data


def skill_dirs():
    found = sorted(ROOT.glob("skills/*/SKILL.md")) + sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))
    return [p.parent for p in found]


def agent_files():
    return sorted(ROOT.glob("agents/*.md")) + sorted(ROOT.glob("plugins/*/agents/*.md"))


def check_skills(max_description, errors):
    names = {}
    for d in skill_dirs():
        rel = d.relative_to(ROOT)
        fm = read_frontmatter(d / "SKILL.md", errors)
        if fm is None:
            continue
        name = fm.get("name")
        if name != d.name:
            errors.append(f"{rel}: frontmatter name {name!r} does not match directory {d.name!r}")
        if d.name in names:
            errors.append(f"{rel}: duplicate skill name, also in {names[d.name]}")
        names[d.name] = rel
        desc = fm.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"{rel}: missing description")
        else:
            if "<" in desc or ">" in desc:
                errors.append(f"{rel}: description contains '<' or '>' (breaks XML-based skill loaders)")
            if len(desc) > max_description:
                errors.append(f"{rel}: description has {len(desc)} characters (limit {max_description})")
        if fm.get("disable-model-invocation") and d.name not in MANUAL_ONLY_ALLOWLIST:
            errors.append(f"{rel}: disable-model-invocation is set but the skill is not in MANUAL_ONLY_ALLOWLIST")
    return names


def check_agents(errors):
    names = set()
    for f in agent_files():
        fm = read_frontmatter(f, errors)
        if fm is None:
            continue
        rel = f.relative_to(ROOT)
        if fm.get("name") != f.stem:
            errors.append(f"{rel}: agent name {fm.get('name')!r} does not match file name {f.stem!r}")
        if not isinstance(fm.get("description"), str) or not fm["description"].strip():
            errors.append(f"{rel}: agent is missing a description")
        names.add(f.stem)
    return names


def check_packs(skills, errors):
    path = ROOT / "config" / "packs.json"
    try:
        packs = json.loads(path.read_text(encoding="utf-8"))["packs"]
    except (OSError, json.JSONDecodeError, KeyError) as e:
        errors.append(f"config/packs.json: cannot be read ({e})")
        return
    for pack, entries in packs.items():
        if entries == "ALL":
            continue
        if not isinstance(entries, list):
            errors.append(f"config/packs.json: pack {pack!r} must be a list or \"ALL\"")
            continue
        for name in entries:
            if name not in skills:
                errors.append(f"config/packs.json: pack {pack!r} lists unknown skill {name!r}")
        dupes = {n for n in entries if entries.count(n) > 1}
        if dupes:
            errors.append(f"config/packs.json: pack {pack!r} repeats {sorted(dupes)}")


def check_router(skills, agents, errors):
    for router in [d / "SKILL.md" for d in skill_dirs() if d.name == "god"]:
        for lineno, line in enumerate(router.read_text(encoding="utf-8").splitlines(), 1):
            if "Activa" not in line:
                continue
            for name in re.findall(r"`/?([a-z][a-z0-9-]*)`", line):
                if name not in skills and name not in agents:
                    errors.append(f"{router.relative_to(ROOT)}:{lineno}: routes to unknown skill or agent {name!r}")


def check_third_party(skills, errors):
    path = ROOT / "THIRD_PARTY.md"
    if not path.exists():
        errors.append("THIRD_PARTY.md is missing")
        return
    listed = set(re.findall(r"`([a-z0-9-]+)`", path.read_text(encoding="utf-8")))
    for name in sorted(skills):
        if name not in listed:
            errors.append(f"THIRD_PARTY.md: skill {name!r} is not listed as third-party or original")


def check_plugins(errors):
    for manifest in sorted(ROOT.glob("plugins/*/.claude-plugin/plugin.json")) + sorted(ROOT.glob(".claude-plugin/*.json")):
        rel = manifest.relative_to(ROOT)
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON ({e})")
            continue
        if manifest.name == "plugin.json":
            name = data.get("name", "")
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or ""):
                errors.append(f"{rel}: plugin name {name!r} must be kebab-case")
            if name != manifest.parent.parent.name:
                errors.append(f"{rel}: plugin name {name!r} does not match directory {manifest.parent.parent.name!r}")
        if manifest.name == "marketplace.json":
            for entry in data.get("plugins", []):
                src = entry.get("source", "")
                if isinstance(src, str) and not (ROOT / src / ".claude-plugin" / "plugin.json").exists():
                    errors.append(f"{rel}: plugin {entry.get('name')!r} points to missing source {src!r}")


def check_protocol(errors):
    for protocol in ROOT.glob("plugins/*/skills/god/references/protocol.md"):
        body = protocol.read_text(encoding="utf-8").split("\n", 1)[1].strip()
        claude_md = (ROOT / "config" / "CLAUDE.md").read_text(encoding="utf-8")
        if body not in claude_md:
            errors.append(f"{protocol.relative_to(ROOT)}: protocol text differs from config/CLAUDE.md; keep both identical")


def check_router_plugin_map(errors):
    location = {d.name: d.parent.parent.name for d in skill_dirs() if d.parent.parent.parent.name == "plugins"}
    for router in [d / "SKILL.md" for d in skill_dirs() if d.name == "god"]:
        text = router.read_text(encoding="utf-8")
        if "## Dónde vive cada skill" not in text:
            continue
        section = text.split("## Dónde vive cada skill", 1)[1]
        for line in section.splitlines():
            m = re.match(r"\|\s*`(god-mode-[a-z]+)`\s*\|[^|]*\|(.*)\|", line)
            if not m:
                continue
            for name in re.findall(r"`([a-z0-9-]+)`", m.group(2)):
                if location.get(name) != m.group(1):
                    errors.append(f"{router.relative_to(ROOT)}: plugin map lists {name!r} under {m.group(1)} "
                                  f"but it lives in {location.get(name, 'no plugin')}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--max-description", type=int, default=DEFAULT_MAX_DESCRIPTION)
    args = parser.parse_args()

    errors = []
    skills = check_skills(args.max_description, errors)
    agents = check_agents(errors)
    check_packs(skills, errors)
    check_router(skills, agents, errors)
    check_third_party(skills, errors)
    check_plugins(errors)
    check_protocol(errors)
    check_router_plugin_map(errors)

    if errors:
        print(f"❌ {len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✅ {len(skills)} skills and {len(agents)} agents are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
