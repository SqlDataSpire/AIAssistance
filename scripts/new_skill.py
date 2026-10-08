#!/usr/bin/env python3
"""Create a new skill from the template inside an existing group.

Usage:
  python scripts/new_skill.py <group-name> <skill-name> "<description>"
"""
import argparse
import re
import sys

from _repo import NAME_RE, PLUGINS, TEMPLATE, group_version, groups, set_skill_version, skills

ap = argparse.ArgumentParser()
ap.add_argument("group")
ap.add_argument("name")
ap.add_argument("description")
args = ap.parse_args()

gdir = PLUGINS / args.group
if not gdir.is_dir():
    names = ", ".join(g.name for g in groups()) or "(none)"
    sys.exit(f"No group '{args.group}'. Existing groups: {names}. "
             "Create one with scripts/new_group.py.")
if not NAME_RE.match(args.name) or len(args.name) > 64:
    sys.exit("Skill name must be lowercase letters, numbers and hyphens (max 64).")
for g in groups():
    if any(s.name == args.name for s in skills(g)):
        sys.exit(f"A skill named '{args.name}' already exists in group '{g.name}'.")
if len(args.description) > 1024:
    sys.exit("Description must be 1024 characters or fewer.")

text = TEMPLATE.read_text(encoding="utf-8")
text = re.sub(r"^name: .*$", f"name: {args.name}", text, count=1, flags=re.M)
desc = args.description.replace("\\", "\\\\").replace('"', '\\"')
text = re.sub(r"^description: .*$", lambda _: f'description: "{desc}"', text, count=1, flags=re.M)
title = args.name.replace("-", " ").title()
text = text.replace("# My Skill Name", f"# {title}", 1)

text = set_skill_version(text, group_version(gdir))

sdir = gdir / "skills" / args.name
sdir.mkdir(parents=True)
(sdir / "SKILL.md").write_text(text, encoding="utf-8")
gitkeep = gdir / "skills" / ".gitkeep"
if gitkeep.exists():
    gitkeep.unlink()

print(f"Created {sdir.relative_to(PLUGINS.parent)}/SKILL.md")
print(f"Next: write the instructions, add a row to plugins/{args.group}/README.md, "
      "then run python scripts/validate_skills.py")
