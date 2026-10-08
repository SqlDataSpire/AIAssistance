#!/usr/bin/env python3
"""Version, changelog, commit and tag one skill group.

Usage:
  python scripts/release.py <group> <patch|minor|major|X.Y.Z> [--push] [--dry-run]

What it does:
  1. Sets the new version in the group's three manifests and in every
     SKILL.md (metadata.version) in the group.
  2. Prepends a section to plugins/<group>/CHANGELOG.md listing the commits
     that touched the group since its previous tag.
  3. Runs the validator.
  4. Commits and creates the annotated tag  <group>--v<version>.
  5. With --push, pushes the commit and the tag (which triggers the GitHub
     release with that group's skill zips).

Passing the group's current version tags it without bumping (useful for the
very first tag).
"""
import argparse
import datetime
import re
import subprocess
import sys

from _repo import (PLUGINS, ROOT, group_version, load_json, set_skill_version, skills,
                   tag_name, write_json)

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout.strip()


def next_version(current: str, bump: str) -> str:
    if SEMVER.match(bump):
        return bump
    m = SEMVER.match(current)
    if not m:
        sys.exit(f"Current version '{current}' is not X.Y.Z; pass an explicit version.")
    major, minor, patch = map(int, m.groups())
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    sys.exit("Bump must be patch, minor, major, or an X.Y.Z version.")


ap = argparse.ArgumentParser()
ap.add_argument("group")
ap.add_argument("bump")
ap.add_argument("--push", action="store_true")
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

gdir = PLUGINS / args.group
if not (gdir / "plugin.json").exists():
    sys.exit(f"No group '{args.group}' under plugins/.")

current = group_version(gdir)
new = next_version(current, args.bump)
tag = tag_name(args.group, new)

if git("tag", "-l", tag):
    sys.exit(f"Tag {tag} already exists.")
if git("status", "--porcelain") and not args.dry_run:
    sys.exit("Working tree has uncommitted changes. Commit or stash them first, "
             "so the tag points at exactly what you meant to release.")

prev_tags = git("tag", "-l", f"{args.group}--v*", "--sort=-v:refname").splitlines()
prev = prev_tags[0] if prev_tags else None
log_range = [f"{prev}..HEAD"] if prev else ["HEAD"]
commits = git("log", *log_range, "--pretty=format:- %s (%h)", "--", f"plugins/{args.group}").splitlines()

print(f"Group:    {args.group}")
print(f"Version:  {current} -> {new}")
print(f"Tag:      {tag}")
print(f"Previous: {prev or '(none)'}")
print(f"Commits:  {len(commits)}")
if args.dry_run:
    print("\n".join(commits) or "(no commits touching this group)")
    print("\nDry run: nothing changed.")
    sys.exit(0)

# 1. versions
for rel in ("plugin.json", ".claude-plugin/plugin.json", "gemini-extension.json"):
    path = gdir / rel
    data = load_json(path)
    data["version"] = new
    write_json(path, data)
for s in skills(gdir):
    md = s / "SKILL.md"
    if md.exists():
        md.write_text(set_skill_version(md.read_text(encoding="utf-8"), new), encoding="utf-8")

# 2. changelog
cl = gdir / "CHANGELOG.md"
head = "# Changelog\n\n"
body = cl.read_text(encoding="utf-8") if cl.exists() else head
if body.startswith(head):
    body = body[len(head):]
section = f"## {new} ({datetime.date.today().isoformat()})\n\n" + \
          ("\n".join(commits) if commits else "- Initial tagged release") + "\n\n"
cl.write_text(head + section + body, encoding="utf-8")

# 3. validate
r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_skills.py")], cwd=ROOT)
if r.returncode != 0:
    sys.exit("Validation failed. Nothing committed; fix the errors (or `git checkout .`) and retry.")

# 4. commit + tag
git("add", f"plugins/{args.group}")
if git("diff", "--cached", "--name-only"):
    git("commit", "-m", f"release({args.group}): v{new}")
git("tag", "-a", tag, "-m", f"{args.group} v{new}")
print(f"\nCommitted and tagged {tag}.")

# 5. push
if args.push:
    git("push")
    git("push", "origin", tag)
    print("Pushed. The GitHub release workflow will attach this group's skill zips.")
else:
    print(f"Push when ready:  git push && git push origin {tag}")
