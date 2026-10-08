#!/usr/bin/env python3
"""Validate every group and skill against the Agent Skills spec, and check that
the per-group manifests and both marketplaces agree with the folder layout.

Usage:  python scripts/validate_skills.py      (exit code 1 on any error)
"""
import json
import sys

from _repo import (CLAUDE_MARKETPLACE, CODEX_MARKETPLACE, NAME_RE, ROOT, groups,
                   load_json, parse_frontmatter, skill_version, skills)

errors: list[str] = []
warnings: list[str] = []


def rel(p):
    return p.relative_to(ROOT).as_posix()


def load(path):
    if not path.exists():
        errors.append(f"missing {rel(path)}")
        return {}
    try:
        return load_json(path)
    except json.JSONDecodeError as e:
        errors.append(f"{rel(path)}: invalid JSON ({e})")
        return {}


def check_skill(sdir, seen, version):
    md = sdir / "SKILL.md"
    if not md.exists():
        errors.append(f"{rel(sdir)}: missing SKILL.md")
        return
    text = md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        errors.append(f"{rel(md)}: frontmatter missing 'name'")
    elif name != sdir.name:
        errors.append(f"{rel(md)}: name '{name}' must match folder '{sdir.name}'")
    elif not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{rel(md)}: name must be lowercase-hyphenated, max 64 chars")
    if not desc:
        errors.append(f"{rel(md)}: frontmatter missing 'description'")
    elif len(desc) > 1024:
        errors.append(f"{rel(md)}: description is {len(desc)} chars (max 1024)")
    if text.count("\n") + 1 > 500:
        warnings.append(f"{rel(md)}: over 500 lines; move detail into reference files")
    sv = skill_version(text)
    if version and sv != version:
        errors.append(f"{rel(md)}: metadata.version is '{sv or '(missing)'}', group version is '{version}' "
                      "(run scripts/release.py, or set it to match)")
    if sdir.name in seen:
        errors.append(f"skill '{sdir.name}' exists in both '{seen[sdir.name]}' and '{sdir.parent.parent.name}'")
    seen[sdir.name] = sdir.parent.parent.name


def check_group(g, seen):
    claude = load(g / ".claude-plugin" / "plugin.json")
    portable = load(g / "plugin.json")
    gemini = load(g / "gemini-extension.json")
    for label, m in (("claude", claude), ("plugin.json", portable), ("gemini", gemini)):
        if m and m.get("name") != g.name:
            errors.append(f"{rel(g)}: {label} manifest name '{m.get('name')}' must be '{g.name}'")
    versions = {"plugin.json": portable.get("version"),
                ".claude-plugin/plugin.json": claude.get("version"),
                "gemini-extension.json": gemini.get("version")}
    if len(set(versions.values())) != 1 or None in versions.values():
        errors.append(f"{rel(g)}: versions must all match: "
                      + ", ".join(f"{k}={v}" for k, v in versions.items()))
    sk = skills(g)
    if not sk:
        warnings.append(f"{rel(g)}: group has no skills yet")
    for s in sk:
        check_skill(s, seen, portable.get("version"))


def check_marketplaces(group_names):
    claude = load(CLAUDE_MARKETPLACE)
    codex = load(CODEX_MARKETPLACE)
    for label, mp, path_of in (
        ("Claude marketplace", claude, lambda e: e.get("source")),
        ("Codex marketplace", codex, lambda e: (e.get("source") or {}).get("path")),
    ):
        if not mp:
            continue
        listed = {}
        for e in mp.get("plugins", []):
            listed[e.get("name")] = path_of(e)
        for name in group_names - listed.keys():
            errors.append(f"{label}: group '{name}' is not listed (run new_group.py or add it)")
        for name in listed.keys() - group_names:
            errors.append(f"{label}: lists '{name}' but plugins/{name}/ does not exist")
        for name, path in listed.items():
            if name in group_names and path != f"./plugins/{name}":
                errors.append(f"{label}: '{name}' source should be './plugins/{name}', got '{path}'")


if __name__ == "__main__":
    gs = groups()
    seen: dict[str, str] = {}
    for g in gs:
        check_group(g, seen)
    check_marketplaces({g.name for g in gs})
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\nChecked {len(gs)} group(s), {len(seen)} skill(s): "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)
