# AIAssistance

[![Validate skills](https://github.com/SqlDataSpire/AIAssistance/actions/workflows/validate.yml/badge.svg)](https://github.com/SqlDataSpire/AIAssistance/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

An open, community collection of reusable **Agent Skills**, organized into installable groups. Each skill is written once and works in Claude, ChatGPT / Codex, Gemini CLI, MiniMax, Cursor, GitHub Copilot, and other assistants that support the open [Agent Skills](https://agentskills.io) standard.

---

## 📦 Skill Groups

Install a whole group, or pick individual skills.

| Group | Skills | Description |
| :--- | :--- | :--- |
| [**`learning`**](./plugins/learning) | `quiz-coach` | Study, quiz, and self-assessment skills for any subject: exams, certifications, courses, and interview prep. |
| [**`atlassian`**](./plugins/atlassian) | `confluence-task-tracker` | Jira and Confluence workflow skills. Needs an Atlassian connector. |
| [**`workflow`**](./plugins/workflow) | `collaboration` | Collaboration protocols and working-style skills for planning, design, and documentation. |

---

## 🚀 Install

| Platform | Install a group | Install one skill |
| :--- | :--- | :--- |
| **Claude Code** | `/plugin marketplace add SqlDataSpire/AIAssistance` then `/plugin install learning@sqldataspire` | via `npx skills` (below) |
| **Claude Desktop / Cowork** | Plugins settings → Add marketplace → `SqlDataSpire/AIAssistance` → pick a group | Upload a skill `.zip` |
| **OpenAI Codex / ChatGPT desktop** | `codex plugin marketplace add SqlDataSpire/AIAssistance`, then install a group from `/plugins` | via `npx skills` |
| **Gemini CLI** | Clone the repo, then `gemini extensions install ./plugins/learning` | `npx skills add SqlDataSpire/AIAssistance -a gemini-cli --skill quiz-coach` |
| **Any agent (Cursor, Copilot, Windsurf, MiniMax Code, OpenCode, …)** | `npx skills add SqlDataSpire/AIAssistance` | `npx skills add SqlDataSpire/AIAssistance --skill quiz-coach` |
| **Upload-based apps (Claude.ai, ChatGPT, MiniMax Agent)** | — | Download `<skill>.zip` from [Releases](https://github.com/SqlDataSpire/AIAssistance/releases) and upload it |

Full instructions, including manual copy installs, are in **[INSTALL.md](./INSTALL.md)**.

---

## 📂 Repository Structure

```
AIAssistance/
├── .claude-plugin/marketplace.json   # Claude marketplace (also read by ChatGPT, npx skills)
├── .agents/plugins/marketplace.json  # Codex / ChatGPT marketplace
├── plugins/
│   ├── learning/                     # ← one folder per group
│   │   ├── .claude-plugin/plugin.json
│   │   ├── plugin.json               # Portable Agent Plugins manifest (Codex / ChatGPT)
│   │   ├── gemini-extension.json
│   │   ├── README.md
│   │   ├── CHANGELOG.md              # Written by release.py
│   │   └── skills/quiz-coach/SKILL.md
│   └── workflow/
│       └── … same layout …
├── scripts/
│   ├── new_group.py                  # Scaffold + register a new group
│   ├── new_skill.py                  # Create a skill in a group from the template
│   ├── validate_skills.py            # Spec + manifest consistency checks (runs in CI)
│   ├── package_skills.py             # Build one upload-ready .zip per skill
│   └── release.py                    # Bump version, changelog, commit + tag <group>--vX.Y.Z
├── templates/SKILL.template.md
├── .github/workflows/                # CI validation + release zips
├── INSTALL.md
├── CONTRIBUTING.md
└── tools/openclaw/                   # Windows: SSH tunnel + app-window launcher for a remote OpenClaw
```

---

## ➕ Contributing

```bash
python scripts/new_skill.py learning flash-cards "Use when the user wants flashcards or spaced repetition."
# new group:
python scripts/new_group.py sql-data "SQL and data engineering helpers." --category Development
python scripts/validate_skills.py
```

See **[CONTRIBUTING.md](./CONTRIBUTING.md)** for details.

## 📄 License

[MIT](./LICENSE)
