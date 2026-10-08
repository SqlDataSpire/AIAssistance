# Confluence patterns for the tracker

Write all page bodies as **HTML** (`contentFormat: "html"`). Send only the body fragment: no `<html>` or `<body>` wrappers and no Markdown fences. If you're unsure of the current HTML rules, call `getContentFormatGuide` with `{ "toolName": "createConfluencePage" }` (or `updateConfluencePage`). The patterns below cover normal tracker operations.

Placeholders: `{SPACE_KEY}`, `{HUB_PAGE_ID}`, `{PAGE_ID}`. Fill them in from the config or from discovery (see SKILL.md §0).

Page URL form: `/wiki/spaces/{SPACE_KEY}/pages/{PAGE_ID}`

## Status and priority lozenges

```html
<span data-type="status" data-color="COLOR">LABEL</span>
```

Status colors: Not started = `neutral`, In progress = `blue`, In review = `yellow`, Blocked = `red`, Waiting = `purple`, Done = `green`.
Priority colors: High = `red`, Medium = `yellow`, Low = `neutral`.

## Dates

Always use a real calendar date, never plain text:

```html
<time datetime="2026-09-30">Sep 30, 2026</time>
```

## Task items

Variants for open, done, prioritized and waiting tasks. Waiting items still count as open, but the brief reports them under Waiting.

```html
<ul data-type="task-list">
  <li data-type="task-item"><input type="checkbox"> Plain open task</li>
  <li data-type="task-item"><input type="checkbox" checked> Completed task</li>
  <li data-type="task-item"><input type="checkbox"> <span data-type="status" data-color="red">High</span> Prioritized task <time datetime="2026-10-03">Oct 3, 2026</time></li>
  <li data-type="task-item"><input type="checkbox"> <span data-type="status" data-color="purple">Waiting</span> Task text, trigger: vendor CSV <time datetime="2026-10-03">Oct 3, 2026</time></li>
</ul>
```

To complete a task, add `checked` to its `<input>`; to reopen it, remove `checked`. Keep any existing `data-local-id` on `<li>` and `<ul>` elements.

---

## Hub page template

Title: `Project & Task Tracker`. Create it in `{SPACE_KEY}`, under the parent page the user chose, if any.

```html
<div data-type="panel-info"><p>Index of active projects. <strong>Status, Priority, Next action and Last updated live only in this table.</strong> Details are on each project's page. Standalone items are on <em>Loose Tasks</em>; saved morning briefs are on <em>Daily Log</em>.</p></div>

<h2>Active projects</h2>
<table>
  <thead>
    <tr><th>Project</th><th>Status</th><th>Priority</th><th>Next action</th><th>Last updated</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><em>Example project (replace me)</em></td>
      <td><span data-type="status" data-color="neutral">Not started</span></td>
      <td><span data-type="status" data-color="neutral">Low</span></td>
      <td><em>First next action</em></td>
      <td><time datetime="YYYY-MM-DD">Mon DD, YYYY</time></td>
    </tr>
  </tbody>
</table>
```

## Hub table row

Add or edit one `<tr>` inside `<tbody>`. Leave the header and the other rows untouched. The Project cell links to the project page.

```html
<tr>
  <td><a href="/wiki/spaces/{SPACE_KEY}/pages/{PAGE_ID}">PROJECT_NAME</a></td>
  <td><span data-type="status" data-color="blue">In progress</span></td>
  <td><span data-type="status" data-color="yellow">Medium</span></td>
  <td>NEXT_ACTION_TEXT</td>
  <td><time datetime="2026-09-30">Sep 30, 2026</time></td>
</tr>
```

When you add the first real project, delete the italic example row if it's still there.

## Project page template

Create it under the hub (`parentId: {HUB_PAGE_ID}`). Title = the project name. Pass the raw name and don't HTML-escape `&` in the title. Leave out the "Waiting on" section unless the project is waiting.

```html
<div data-type="panel-info"><p><strong>Objective.</strong> ONE_LINE_OBJECTIVE</p></div>

<h2>Current state</h2>
<p>Where we left off: SHORT_NOTE.</p>

<h2>Waiting on</h2>
<div data-type="panel-warning"><p><strong>Waiting on:</strong> TRIGGER, expected <time datetime="YYYY-MM-DD">Mon DD, YYYY</time>.</p></div>

<h2>Tasks</h2>
<ul data-type="task-list">
  <li data-type="task-item"><input type="checkbox"> FIRST_TASK</li>
</ul>

<h2>Links</h2>
<ul>
  <li><a href="URL" data-card-appearance="inline"></a></li>
</ul>

<h2>Notes</h2>
<p><em>Running notes and decisions.</em></p>
```

## Loose Tasks page template

Title: `Loose Tasks`, as a child of the hub.

```html
<div data-type="panel-info"><p>Standalone check-off items that don't belong to a project. Move an item to a project page when it grows.</p></div>

<h2>Open</h2>
<ul data-type="task-list">
  <li data-type="task-item"><input type="checkbox"> <em>Example loose task (replace me)</em></li>
</ul>

<h2>Done</h2>
<ul data-type="task-list">
</ul>
```

## Daily Log page template

Title: `Daily Log`, as a child of the hub.

```html
<div data-type="panel-info"><p>Saved morning briefs, newest first.</p></div>
```

## Daily Log entry template

Insert at the top of the Daily Log body, right after the intro info panel, so the newest entry comes first:

```html
<h2><time datetime="YYYY-MM-DD">Mon DD, YYYY</time>: SHORT_TITLE</h2>
<ul>
  <li><strong>Done:</strong> WHAT_MOVED</li>
  <li><strong>Where we left off:</strong> STATE_NOW</li>
  <li><strong>Next:</strong> IMMEDIATE_NEXT_STEP</li>
</ul>
```

## Reading for the brief

- **Hub table:** status, priority, next action and last updated for each project.
- **Each project page:** Current state, open (unchecked) tasks, and the Waiting-on panel.
- **Loose Tasks, "Open" list:** standalone open items.
- **Stale** means the last-updated date is `staleDays` (default 3) or more days before today.
