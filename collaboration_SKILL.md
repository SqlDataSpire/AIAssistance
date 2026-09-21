---
name: collaboration
description: Dual-mode collaboration protocol for game mechanics brainstorming (Suggestion mode) and documentation commits (Decision mode).
---

# Collaboration Skill Instructions

When collaborating on game design, architecture, or codebase developments, always adhere to the following two-mode protocol based on the user's prompt prefix:

## 1. Suggestion Mode
* **Trigger**: Prompts starting with or prefixed by **"Suggestion"**.
* **Behavior**:
  * Analyze proposed ideas deeply by weighing **pros vs. cons**.
  * Examine potential ripple effects, mechanical traps, and balance consequences.
  * Ask clarifying questions and double-check edge cases before taking action.
  * **Rule**: Do NOT modify or commit changes to official documentation files during this phase.

## 2. Decision Mode
* **Trigger**: Prompts starting with or prefixed by **"Decision"**.
* **Behavior**:
  * Commit confirmed choices immediately into official documentation (e.g., `MASTER_MALADY_GAME_DESIGN.md`).
  * **Rule**: **NEVER overwrite or delete historical text**. Always preserve replaced or evolved mechanics using ~~strikethrough formatting~~, followed immediately by the new decision details.
