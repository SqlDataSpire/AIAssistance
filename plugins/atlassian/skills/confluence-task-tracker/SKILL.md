---
name: confluence-task-tracker
description: Track projects and tasks in Confluence. Keeps a hub page with a status table, one page per project, a Loose Tasks page and a Daily Log; creates projects and tasks, updates statuses (including Blocked vs Waiting on an external trigger), and produces a daily "morning brief". Use whenever the user mentions their projects, tasks, to-dos or checklist; asks "where are we", "what's next", "where did we leave off", or for a morning brief, daily summary or standup; marks something done, blocked, waiting, in review or in progress; or adds a new project or task, even without saying "Confluence". Requires a Confluence connection (e.g. the Atlassian MCP server).
metadata:
  version: "1.0.0"
---

# Confluence Task Tracker

This skill runs a small tracker made of four kinds of Confluence pages:

- **Hub** (`Project & Task Tracker`): the index, with an at-a-glance table of every project.
- **Project pages**: one child page of the hub per project.
- **Loose Tasks**: check-off items that don't belong to any project.
- **Daily Log**: dated entries saved from morning briefs.

All HTML patterns and page templates are in [`references/confluence.md`](references/confluence.md). **Read it before creating or editing any page.**

The examples use the Atlassian MCP server's tool names (`getConfluencePage`, `updateConfluencePage`, `createConfluencePage`, `searchConfluenceUsingCql`, `getAccessibleAtlassianResources`). If the connector exposes different names, use the equivalent tools.

---

## 0. Locate the tracker (every session)

You need these values: **site** and **cloudId**, **space key**, and the page IDs of the **hub**, **Daily Log** and **Loose Tasks** pages. Resolve them in this order and stop at the first that works:

1. **Config file.** If you can read files, look for `.confluence-tracker.json` in the current project folder, then `~/.config/confluence-task-tracker/config.json`. The format is in [`config.example.json`](config.example.json).
2. **Discovery.**
   - `getAccessibleAtlassianResources` → site URL and cloudId. If there are several sites, ask which one to use.
   - `searchConfluenceUsingCql` with `type = page AND title = "Project & Task Tracker"` (add `AND space = "<KEY>"` if the space is known) → hub page ID and space key.
   - Get the hub's child pages and pick out `Daily Log` and `Loose Tasks` by title. Every other child page is a project page.
   - If more than one hub matches, ask which one to use.
3. **First-time setup.** If no hub exists, offer to create one (see §1).

After discovery or setup, if you can write files, offer **once** to save the values to a config file so later sessions skip the lookup. Never put API tokens or passwords in the config; the connection handles authentication.

If the Atlassian tools aren't loaded, search the available tools for "confluence" first. If there's no Confluence connection at all, tell the user that this skill needs one.

---

## 1. First-time setup

Ask in one message: **which space** to use (key or name) and an optional **parent page** to put the tracker under. Then:

1. Create the **hub** page from the *Hub page template*.
2. Create **Daily Log** and **Loose Tasks** as children of the hub from their templates.
3. Report the three page links, and offer to save the config (§0).

Confirm the plan in one line before creating anything.

---

## Status vocabulary

| Status | Color | Meaning |
| :--- | :--- | :--- |
| Not started | neutral | Defined but not begun |
| In progress | blue | Actively being worked on |
| In review | yellow | Work done, awaiting review or verification |
| Blocked | red | Stuck because something is wrong and needs intervention |
| Waiting | purple | Paused for an expected external event. Must have a **named trigger** and optionally a date. |
| Done | green | Complete |

Priority: **High** = red, **Medium** = yellow, **Low** = neutral.

**Blocked vs Waiting:** use **Waiting** when the hold-up is a normal, expected external event (a vendor file, someone's sign-off, a scheduled run), and record what it's waiting on plus a date to watch. Use **Blocked** when something has gone wrong.

## Where each fact lives

- **Status, Priority, Next action and Last updated** live **only** in the project's row of the hub table.
- The **project page** holds the objective, current state ("where we left off"), what it's waiting on, the task checklist, links and notes.
- So updating a project usually touches **two** pages: its hub row and its project page.

## Editing a page safely

1. Fetch the current body with `getConfluencePage` (`contentFormat: "html"`).
2. Edit only the part you need. **Keep everything else exactly as it was**, especially `data-local-id` attributes, macros, and other tables and rows.
3. Write it back with `updateConfluencePage` (`contentFormat: "html"`) and a short `versionMessage`.
4. Use the real current date in every `<time>` element.
5. If a fetched page looks incomplete or an update fails, stop and explain. Never write back a partial page body.

**Confirm before writing:** state the concrete change in one line and get a clear yes. The **morning brief is read-only**.

---

## Operations

Each operation needs a few answers. Ask for any missing ones in **one compact message**, use sensible defaults, and let the user correct you. Don't re-ask anything the user already said.

### 1. New project
Ask for: **name**, one-line **objective**, **status** (default In progress), **priority**, the **first next action**, any **starter tasks**, and whether it's **waiting on an external trigger** (if so, what and an optional date).

Then:
- Create the project page under the hub from the *Project page template*.
- Add a row to the hub table, with the project name linking to the new page. If the italic example row is still there, replace it.
- If it's waiting, set the status to Waiting and fill in the "Waiting on" panel.

### 2. New task
Ask for: the **task text**, **which project** (or standalone), and optionally **priority**, **due date**, and **waiting on**.

Add a checkbox item (see the task-item patterns) to the project page's Tasks list, or to the "Open" list on Loose Tasks if it's standalone.

### 3. Move a task to a project
Remove the `<li>` from the source page (Loose Tasks or the wrong project), add it to the target project's Tasks list, and save both pages. Confirm in one line first.

### 4. Update status
Users phrase updates naturally: "the API project is in review", "checked off the schema fix", "billing is waiting on the vendor file until Friday", "unblock the migration".

- **Project status**: update the Status lozenge in the hub row and refresh Next action and Last updated. If the update implies a new "where we left off", update Current state on the project page. For Waiting, fill in the project page's Waiting-on panel with the trigger and date.
- **Task done or reopened**: add or remove `checked` on the task's checkbox. If it was the project's last open task, say so.
- Always update **Last updated** on the hub row of every project you touched.

### 5. Morning brief ("morning brief", "where are we", "standup")

**Read-only.** Read the hub table, each active project page (current state, open tasks, waiting on) and the "Open" list on Loose Tasks. Report in this format, leaving out empty sections:

```
# Morning brief: <today's date>

## In focus  (In progress / In review, highest priority first)
- <Project>: <status> · next: <next action> · <N> open tasks
  - <open task>

## Waiting on external triggers
- <Project>: waiting on <trigger> (expected <date>)   ← flag if the date is today or past

## Blocked
- <Project>: <what's blocking it>

## Loose tasks
- [ ] <open item>

## Stale  (no update in 3+ days, or the configured staleDays)
- <Project>: last updated <date>

## Not started / backlog
- <Project>: <priority>
```

End with one line, **Suggested first move today:**, pointing at the highest-priority next action.

Only if the user then says "log it" or "save the brief": add a dated entry at the top of the Daily Log using the *Daily Log entry template*, and update Last updated on any projects mentioned. Confirm before writing.

---

## Notes

- Keep status replies short and conversational. The pages hold the detail.
- Don't import from other Confluence pages or from Jira unless the user asks. The tracker is a hand-built list.
- To link a Jira issue (e.g. `PROJ-123`), put its full browse URL in the project page's Links section as an inline card.
