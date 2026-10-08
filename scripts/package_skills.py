#!/usr/bin/env python3
"""Zip each skill into dist/<skill-name>.zip for upload-based platforms
(ChatGPT / OpenAI API, Claude.ai, MiniMax, and others).

Each zip holds one top-level folder with exactly one SKILL.md.
Usage:  python scripts/package_skills.py [--group <group>]
"""
import argparse
import shutil
import zipfile

from _repo import ROOT, groups, skills

ap = argparse.ArgumentParser()
ap.add_argument("--group", help="only package this group")
args = ap.parse_args()

DIST = ROOT / "dist"
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

for g in groups():
    if args.group and g.name != args.group:
        continue
    for s in skills(g):
        if not (s / "SKILL.md").exists():
            continue
        out = DIST / f"{s.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(s.rglob("*")):
                if f.is_file():
                    zf.write(f, f.relative_to(s.parent).as_posix())
        print(f"built dist/{out.name}  ({g.name})")
