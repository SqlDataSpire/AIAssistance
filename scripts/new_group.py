#!/usr/bin/env python3
"""Create a new skill group (plugin) and register it in both marketplaces.

Usage:
  python scripts/new_group.py <group-name> "<description>" [--category Productivity]

Creates plugins/<group-name>/ with Claude, portable (Codex/ChatGPT) and
Gemini manifests, a README, and an empty skills/ folder.
"""
import argparse
import sys

from _repo import (AUTHOR, CLAUDE_MARKETPLACE, CODEX_MARKETPLACE, LICENSE, NAME_RE,
                   PLUGINS, REPO_URL, load_json, write_json)

ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("description")
ap.add_argument("--category", default="Productivity")
ap.add_argument("--version", default="1.0.0")
args = ap.parse_args()

if not NAME_RE.match(args.name):
    sys.exit("Group name must be lowercase letters, numbers and hyphens.")
gdir = PLUGINS / args.name
if gdir.exists():
    sys.exit(f"{gdir.relative_to(PLUGINS.parent)} already exists.")

homepage = f"{REPO_URL}/tree/main/plugins/{args.name}"

write_json(gdir / ".claude-plugin" / "plugin.json", {
    "name": args.name,
    "version": args.version,
    "description": args.description,
    "author": AUTHOR,
    "homepage": homepage,
    "repository": REPO_URL,
    "license": LICENSE,
})
write_json(gdir / "plugin.json", {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": args.name,
    "version": args.version,
    "description": args.description,
    "author": AUTHOR,
    "homepage": homepage,
    "repository": REPO_URL,
    "license": LICENSE,
})
write_json(gdir / "gemini-extension.json", {
    "name": args.name,
    "version": args.version,
    "description": args.description,
})
(gdir / "CHANGELOG.md").write_text("# Changelog\n\n", encoding="utf-8")
(gdir / "skills").mkdir(parents=True)
(gdir / "skills" / ".gitkeep").touch()
(gdir / "README.md").write_text(
    f"# {args.name}\n\n{args.description}\n\n"
    "| Skill | Description |\n| :--- | :--- |\n",
    encoding="utf-8",
)

claude = load_json(CLAUDE_MARKETPLACE)
claude["plugins"].append({
    "name": args.name,
    "source": f"./plugins/{args.name}",
    "description": args.description,
    "category": args.category.lower(),
    "homepage": homepage,
})
write_json(CLAUDE_MARKETPLACE, claude)

codex = load_json(CODEX_MARKETPLACE)
codex["plugins"].append({
    "name": args.name,
    "source": {"source": "local", "path": f"./plugins/{args.name}"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": args.category,
})
write_json(CODEX_MARKETPLACE, codex)

print(f"Created plugins/{args.name}/ and registered it in both marketplaces.")
print(f"Next: python scripts/new_skill.py {args.name} <skill-name> \"<description>\"")
