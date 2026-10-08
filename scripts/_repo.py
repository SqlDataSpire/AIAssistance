"""Shared paths and helpers for the repo scripts."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
TEMPLATE = ROOT / "templates" / "SKILL.template.md"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

AUTHOR = {"name": "Antony Liberato", "url": "https://github.com/SqlDataSpire"}
REPO_URL = "https://github.com/SqlDataSpire/AIAssistance"
LICENSE = "MIT"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def groups():
    """Every plugin group folder under plugins/."""
    if not PLUGINS.exists():
        return []
    return sorted(p for p in PLUGINS.iterdir() if p.is_dir() and not p.name.startswith("."))


def skills(group: Path):
    """Every skill folder in a group."""
    sk = group / "skills"
    if not sk.exists():
        return []
    return sorted(p for p in sk.iterdir() if p.is_dir() and not p.name.startswith("."))


def group_version(group: Path) -> str:
    """The group's version, read from its portable plugin.json."""
    return load_json(group / "plugin.json").get("version", "")


def tag_name(group_name: str, version: str) -> str:
    """Release tag convention: <group>--v<version> (Claude Code's plugin tag format)."""
    return f"{group_name}--v{version}"


def _frontmatter_bounds(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    return None if end == -1 else (text.find("\n") + 1, end + 1)


def skill_version(text: str) -> str:
    """Read metadata.version from SKILL.md frontmatter ('' if absent)."""
    b = _frontmatter_bounds(text)
    if not b:
        return ""
    in_meta = False
    for line in text[b[0]:b[1]].splitlines():
        if re.match(r"^metadata:\s*$", line):
            in_meta = True
            continue
        if in_meta:
            if line and not line.startswith((" ", "\t")):
                break
            m = re.match(r"^\s+version:\s*['\"]?([^'\"\s]+)['\"]?\s*$", line)
            if m:
                return m.group(1)
    return ""


def set_skill_version(text: str, version: str) -> str:
    """Set metadata.version in SKILL.md frontmatter, preserving other metadata keys."""
    b = _frontmatter_bounds(text)
    if not b:
        raise ValueError("SKILL.md has no frontmatter")
    lines = text[b[0]:b[1]].splitlines()
    out, i, done = [], 0, False
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if re.match(r"^metadata:\s*$", line):
            i += 1
            block = []
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i])
                i += 1
            block = [l for l in block if not re.match(r"^\s+version:", l)]
            out.extend([f'  version: "{version}"'] + block)
            done = True
            continue
        i += 1
    if not done:
        out += ["metadata:", f'  version: "{version}"']
    return text[:b[0]] + "\n".join(out) + "\n" + text[b[1]:]


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data
