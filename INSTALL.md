# Installation Guide

Skills live in groups under [`plugins/`](./plugins). Each skill is a folder with a `SKILL.md` in the open [Agent Skills](https://agentskills.io) format, so the same files work on every platform below.

| Group | Skills |
| :--- | :--- |
| `learning` | `quiz-coach` |
| `workflow` | `collaboration` |
| `atlassian` | `confluence-task-tracker` (needs a Jira/Confluence connector) |

---

## Option 1: Install a group as a plugin or extension

### Claude Code
```
/plugin marketplace add SqlDataSpire/AIAssistance
/plugin install learning@sqldataspire
/plugin install workflow@sqldataspire
```
Update later with `/plugin marketplace update sqldataspire`.

### Claude Desktop / Cowork
Plugins settings → **Add marketplace** → `SqlDataSpire/AIAssistance` → install the groups you want.

### OpenAI Codex CLI / ChatGPT desktop
```
codex plugin marketplace add SqlDataSpire/AIAssistance
```
Open `/plugins` (CLI) or the Plugins Directory (ChatGPT desktop), choose **SqlDataSpire Skills**, and install a group. Update later with `codex plugin marketplace upgrade sqldataspire`.

### Gemini CLI
Gemini installs one extension per folder, so clone the repo and install each group you want:
```
git clone https://github.com/SqlDataSpire/AIAssistance
gemini extensions install ./AIAssistance/plugins/learning
```
To pick up changes: `git pull`, then `gemini extensions update learning`. (Or use `npx skills` below, which needs no clone.)

---

## Option 2: Install individual skills with `npx skills`

Works with 70+ agents, including Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, Windsurf, MiniMax Code, OpenCode, Goose, and Antigravity.

```bash
# Choose skills and agents interactively
npx skills add SqlDataSpire/AIAssistance

# One skill
npx skills add SqlDataSpire/AIAssistance --skill quiz-coach

# One skill, specific agents, user-wide
npx skills add SqlDataSpire/AIAssistance --skill quiz-coach -a gemini-cli -a codex -g

# See what's available
npx skills add SqlDataSpire/AIAssistance --list
```
Update later with `npx skills update`.

---

## Option 3: Upload a skill bundle

For apps that install skills from a file (Claude.ai, ChatGPT, MiniMax Agent, and others):

1. Download `<skill-name>.zip` from the [latest release](https://github.com/SqlDataSpire/AIAssistance/releases/latest).
2. Upload it in the app's skills settings (one skill per zip).

To build the zips yourself: `python scripts/package_skills.py` (output in `dist/`).

---

## Option 4: Manual copy

Copy a skill folder (for example `plugins/learning/skills/quiz-coach`) into your assistant's skills directory.

| Assistant | User-wide folder | Project folder |
| :--- | :--- | :--- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| OpenAI Codex | `~/.codex/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.agents/skills/` |
| Antigravity | `~/.gemini/antigravity/skills/` | `.agents/skills/` |
| MiniMax Code | `~/.minimax/skills/` | `.minimax/skills/` |
| Cursor | `~/.cursor/skills/` | `.agents/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.agents/skills/` |

**macOS / Linux**
```bash
cp -r plugins/learning/skills/quiz-coach ~/.claude/skills/
```

**Windows (PowerShell)**
```powershell
Copy-Item -Recurse -Force .\plugins\learning\skills\quiz-coach "$env:USERPROFILE\.claude\skills\"
```

---

## Option 5: Paste into a chat

No skills support? Copy a skill's `SKILL.md` into your project instructions, custom instructions, or the start of a chat.

---

## Pin a specific version

Every group release is tagged `<group>--v<version>` (see the [tags](https://github.com/SqlDataSpire/AIAssistance/tags)). Pin a tag to reproduce a bug or stay on a known-good version.

| Platform | Command |
| :--- | :--- |
| Claude Code | `/plugin marketplace add SqlDataSpire/AIAssistance#learning--v1.0.0` (remove the unpinned marketplace first with `/plugin marketplace remove sqldataspire`, since both share a name) |
| Codex / ChatGPT | `codex plugin marketplace add SqlDataSpire/AIAssistance --ref learning--v1.0.0` |
| Gemini CLI | `git -C AIAssistance checkout learning--v1.0.0`, then `gemini extensions install ./AIAssistance/plugins/learning` |
| `npx skills` | `npx skills add https://github.com/SqlDataSpire/AIAssistance/tree/learning--v1.0.0/plugins/learning/skills/quiz-coach` |
| Zip upload | Download from the matching [release](https://github.com/SqlDataSpire/AIAssistance/releases) |

Pinning the marketplace pins the whole repo at that tag's commit, so other groups come from the same point in history.

---

## Verify it works

- **`collaboration`**: send `Suggestion: what if we…` to get a pros/cons analysis, then `Decision: go with …` to record it in your docs.
- **`quiz-coach`**: ask *"Quiz me on Python basics"* or *"Let's do a mock exam on AWS Cloud Practitioner."*
