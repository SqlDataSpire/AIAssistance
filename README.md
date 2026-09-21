# AIAssistance

A curated repository of reusable AI skills, helper scripts, and automation artifacts to optimize your experience with AI coding assistants (such as Antigravity IDE, Claude Code, Gemini CLI) and LLM platforms.

---

## ⚡ Quick Links

- 📖 **[Skills Installation Guide](./skills/README.md)** – Detailed instructions on installing skills globally or per-workspace.

---

## 🤖 Included AI Skills (`skills/`)

Skills follow the open Agent Skills standard and provide pre-packaged protocols, guidelines, and behavioral modes for AI agents.

| Skill | Category | Description | Location |
| :--- | :--- | :--- | :--- |
| **`collaboration`** | Protocol / Workflow | Dual-mode protocol for game mechanics brainstorming (*Suggestion mode*) and documentation commits (*Decision mode*). | [`skills/collaboration`](./skills/collaboration) |
| **`quiz-coach`** | Learning / Study | Interactive study and diagnostic coach for technical certification exams, interview prep, and guided self-testing. | [`skills/quiz-coach`](./skills/quiz-coach) |

> 💡 *For step-by-step instructions on installing skills into your AI assistant, see the **[Skills Installation Guide](./skills/README.md)**.*

---

## 🛠️ Scripts & Utilities

| Utility | Platform | Description |
| :--- | :--- | :--- |
| **`openclaw_gui.bat`** | Windows | Batch script that automates SSH tunneling to an OpenClaw instance and opens the browser UI. |

---

## 📂 Repository Structure

```
AIAssistance/
├── README.md             # Main repository overview & index
├── openclaw_gui.bat      # OpenClaw SSH tunnel & launcher script
└── skills/               # Reusable AI Agent Skills directory
    ├── README.md         # Detailed skill installation guide
    ├── collaboration/    # Collaboration protocol skill
    └── quiz-coach/       # Quiz & test prep coach skill
```

---

## ➕ Adding New Skills & Utilities

As this repository grows:

1. **Adding a New Skill**:
   - Create a subfolder inside `skills/<skill-name>/`.
   - Add a `SKILL.md` file containing the mandatory YAML frontmatter (`name` and `description`).
   - Add the skill to the table above and in [`skills/README.md`](./skills/README.md).

2. **Adding a New Script / Tool**:
   - Place the script in the root directory (or a designated subfolder).
   - Document its purpose and usage parameters in the **Scripts & Utilities** section above.
