---
name: collaboration
description: Two-mode collaboration protocol for any project (software, product, game design, writing, research, business planning). "Suggestion:" messages get a pros/cons analysis with no changes to official documentation; "Decision:" messages are the only trigger for committing a choice to the project's docs, and every change preserves the history of what was decided before. Use when the user prefixes a message with Suggestion or Decision, asks to weigh options, or wants a running record of how decisions evolved.
metadata:
  version: "1.0.0"
---

# Collaboration Protocol

A working agreement for designing things together. Ideas are explored freely, but nothing becomes official until the user says **Decision**. Every decision is recorded so the full evolution of the project, including what was rejected and why, is never lost.

## The Two Modes

The mode is set by the start of the user's message (case-insensitive, with or without a colon).

| Prefix | Mode | Documentation |
| :--- | :--- | :--- |
| `Suggestion` | Explore and evaluate | 🔒 **Locked.** Do not edit official docs. |
| `Decision` | Commit | ✏️ **Write.** Record the decision now. |
| *(no prefix)* | Normal discussion | 🔒 Locked, the same as Suggestion |

**The gate:** official documentation changes **only** in response to a `Decision` message. If the user seems to settle something without the prefix ("ok let's go with B"), don't write. Ask once: *"Want me to record that as a Decision?"*

---

## 1. Suggestion Mode: Explore Before Committing

**Goal:** help the user see the whole picture before choosing.

For each idea:

1. **Restate it** in one line to confirm you understood.
2. **Pros:** concrete benefits, including who gains and by how much.
3. **Cons:** costs, risks, and complexity, with the same honesty as the pros. Don't soften real problems.
4. **Ripple effects:** what else this touches (other components, earlier decisions, users, timeline, budget, consistency).
5. **Conflicts with prior decisions:** if it contradicts something already decided, say so and cite the decision.
6. **Alternatives:** at least one other approach, including "do nothing" when that's realistic, with a quick pros/cons for each.
7. **Open questions:** what you'd need to know to recommend confidently.
8. **Recommendation (optional):** if the evidence clearly favors one option, say which and why. Make clear it's the user's call.

**Keep a running options list.** As ideas come up, track them in the conversation so they can be captured when a decision is made:

```
Open topic: <topic>
  Option A: <summary>, status: favored / considered / rejected (why)
  Option B: …
```

**Rules:**
- Don't edit official documentation, specs, or design docs.
- Don't make implementation changes based on an unconfirmed idea. Scratch prototypes are fine only if the user asks for one.
- Push back when an idea has a real flaw. Agreeing too easily defeats the purpose.

---

## 2. Decision Mode: Commit with History

**Goal:** turn the user's choice into official documentation, with the reasoning and history kept.

### Step 1: Find the official doc
- Use the project's designated design or decision document. If you don't know which it is, look for an obvious one (e.g. `DESIGN.md`, `SPEC.md`, `docs/`, `DECISIONS.md`, or a project-named design doc).
- If none exists or it's ambiguous, ask once which file to use, or offer to create `docs/DECISIONS.md`. Remember the answer for the rest of the session.
- If you can't edit files in this environment, output the exact text to add so the user can paste it.

### Step 2: Check before writing
Commit right away unless one of these is true. If one is, ask a single short question first:
- The decision is ambiguous: it could mean more than one thing.
- It contradicts an earlier decision and the user didn't say they're replacing it.
- It's missing a detail the docs need (for example a number, a name, or a scope).

### Step 3: Update the document, never erasing history
- **Never delete or overwrite earlier decision text.**
- When a decision changes something already documented, keep the old text with ~~strikethrough~~ and put the new text right after it, with a pointer to the decision record:

  ```markdown
  ~~Players start with 3 lives.~~ Players start with 5 lives. *(D-007, 2026-10-08)*
  ```

- New content that replaces nothing is simply added in the right section.

### Step 4: Add a decision record
Append an entry to the doc's **Decision Log** section, or to the separate log file if the project uses one:

```markdown
### D-007: <short title>
- **Date:** YYYY-MM-DD
- **Status:** Accepted   <!-- Accepted | Superseded by D-0XX | Reversed by D-0XX -->
- **Decision:** <what was decided, one or two sentences>
- **Rationale:** <why — the pros that won>
- **Trade-offs accepted:** <the cons knowingly taken on>
- **Alternatives considered:** <options from the Suggestion discussion and why each was not chosen>
- **Supersedes:** <D-0XX, or "none">
```

- Number decisions sequentially and continue from the last number in the log.
- When a new decision replaces an old one, also update the old record's **Status** to `Superseded by D-0XX`. That status line is the one field you may edit in an old record.
- Fill **Alternatives considered** from the running options list, so rejected ideas and their reasons are kept.

### Step 5: Confirm
Reply with a short summary: the decision ID, which file(s) changed, and what was struck through or added. Close the topic in the running options list.

---

## Quick Reference

| Situation | Do |
| :--- | :--- |
| `Suggestion: what if we…` | Pros, cons, ripple effects, alternatives. No doc edits. |
| `Decision: go with option B` | Update the docs with strikethrough history, add a D-record, confirm. |
| User agrees without the prefix | Ask: "Record that as a Decision?" |
| Decision contradicts D-004 | Ask: "This replaces D-004. Confirm?" Then supersede it. |
| User asks "how did we get here?" | Summarize the decision log for that topic in order. |
| Doc file unknown | Ask once, or offer `docs/DECISIONS.md`. |
