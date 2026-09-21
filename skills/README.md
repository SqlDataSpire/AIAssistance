# Agent Skills Directory & Installation Guide

This directory contains reusable AI Assistant Skills following the open Agent Skills standard. Skills provide pre-packaged instructions, protocols, and workflows that enable AI coding assistants (like Antigravity IDE, Claude Code, Gemini CLI) and general LLMs to follow specific behaviors.

---

## 📦 Included Skills

| Skill | Description | Directory |
| :--- | :--- | :--- |
| **`collaboration`** | Dual-mode collaboration protocol for game mechanics brainstorming (*Suggestion mode*) and documentation commits (*Decision mode*). | [`./collaboration`](../AIAssistance/skills/collaboration) |
| **`quiz-coach`** | Interactive study and assessment coach for certification exams, technical quizzes, and guided self-testing. | [`./quiz-coach`](../AIAssistance/skills/quiz-coach) |

---

## 🛠️ Installation Instructions

Choose the installation method that fits your environment:

### Method 1: Global Installation (Antigravity IDE / Gemini Agent)

To make a skill available across **all your projects** on your computer, copy the skill subfolder into your global skills directory.

#### Windows (PowerShell)
```powershell
# Install a specific skill (e.g., quiz-coach)
Copy-Item -Recurse -Force .\skills\quiz-coach "$env:USERPROFILE\.gemini\config\skills\"

# Or install ALL skills at once
Copy-Item -Recurse -Force .\skills\* "$env:USERPROFILE\.gemini\config\skills\"
```

#### Windows (Command Prompt / CMD)
```cmd
:: Install a specific skill
xcopy /E /I /Y skills\quiz-coach "%USERPROFILE%\.gemini\config\skills\quiz-coach"

:: Install ALL skills
xcopy /E /I /Y skills "%USERPROFILE%\.gemini\config\skills"
```

#### macOS / Linux (Bash or Zsh)
```bash
# Install a specific skill
cp -r ./skills/quiz-coach ~/.gemini/config/skills/

# Or install ALL skills at once
cp -r ./skills/* ~/.gemini/config/skills/
```

*Note: For Claude Code CLI, replace `.gemini/config/skills` with `.claude/skills` in the paths above.*

---

### Method 2: Local Project / Workspace Installation

If you only want to enable a skill within a **specific project repository**:

1. Copy the desired skill directory (e.g., `quiz-coach`) into your target project's `skills/` folder:
   ```powershell
   Copy-Item -Recurse .\skills\quiz-coach "C:\path\to\your-project\skills\"
   ```
2. Your AI coding assistant will automatically detect and load skills stored in the root `skills/` or `.gemini/config/skills/` directory of the active workspace.

---

### Method 3: Web AI Assistants (ChatGPT, Claude.ai, Gemini Web)

If you are using web-based AI tools without local directory access:

1. Navigate into the skill folder (e.g., `skills/quiz-coach/`).
2. Open `SKILL.md`.
3. Copy the entire file content (excluding or including the YAML header).
4. Paste the content into one of the following:
   - **ChatGPT**: Custom Instructions / System Prompt or Custom GPT Instructions.
   - **Claude.ai**: Project Knowledge / Project Instructions.
   - **Direct Prompting**: Paste into your chat prompt at the start of your session.

---

## 📂 Skill Folder Structure

Each skill folder must follow this standard format:

```
skills/
├── README.md (This file)
├── collaboration/
│   └── SKILL.md
└── quiz-coach/
    └── SKILL.md
```

- **`SKILL.md`**: The mandatory entry point containing frontmatter (`name` and `description`) followed by markdown instructions for the AI model.

---

## ✅ Verifying Installation

Once installed, test the skill by chatting with your AI assistant:
- For **`collaboration`**: Prefix your message with `Suggestion:` or `Decision:` to trigger the respective mode.
- For **`quiz-coach`**: Prompt the assistant with *"Quiz me on Python basics"* or *"Let's do a mock exam on AWS Cloud Practitioner"*.
